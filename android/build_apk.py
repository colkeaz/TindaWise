"""
Deterministic Android APK Compiler, Packager, Zipaligner & V1/V2/V3 Signer for TindaWise.
Uses the local Android SDK build-tools (36.0.0), Android 36 platform jar, and Android Studio JBR.

Pipeline:
1. Syncs `src/frontend/index.html` into `android/app/src/main/assets/index.html`.
2. Compiles Android resources (`res/values/strings.xml`, `res/drawable/ic_launcher.xml`) via `aapt2 compile`.
3. Links `AndroidManifest.xml` + compiled resources + `assets/index.html` into an intermediate APK and generates `R.java` via `aapt2 link`.
4. Compiles `MainActivity.java` + `R.java` against `android-36/android.jar` (targeting Java 11 bytecode) via `javac`.
5. Converts `.class` bytecode into `classes.dex` via `d8`.
6. Injects `classes.dex` into the APK archive.
7. Aligns the APK on 4-byte boundaries via `zipalign -p -f -v 4`.
8. Generates a signing keystore (if not present) via `keytool` and signs the APK with V1 + V2 + V3 signatures via `apksigner sign`.
9. Verifies the signed APK via `apksigner verify --verbose` and `aapt2 dump badging`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile

ROOT_DIR = r"C:\Users\Lenovo\Documents\AIdeathon"
ANDROID_DIR = os.path.join(ROOT_DIR, "android")
APP_MAIN = os.path.join(ANDROID_DIR, "app", "src", "main")
BUILD_DIR = os.path.join(ANDROID_DIR, "build")
DIST_DIR = os.path.join(ROOT_DIR, "dist")

SDK_DIR = r"C:\Users\Lenovo\AppData\Local\Android\Sdk"
BUILD_TOOLS = os.path.join(SDK_DIR, "build-tools", "36.0.0")
PLATFORM_JAR = os.path.join(SDK_DIR, "platforms", "android-36", "android.jar")
JBR_BIN = r"C:\Program Files\Android\Android Studio\jbr\bin"

AAPT2 = os.path.join(BUILD_TOOLS, "aapt2.exe")
D8 = os.path.join(BUILD_TOOLS, "d8.bat")
ZIPALIGN = os.path.join(BUILD_TOOLS, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS, "apksigner.bat")
JAVAC = os.path.join(JBR_BIN, "javac.exe")
KEYTOOL = os.path.join(JBR_BIN, "keytool.exe")


def run_cmd(cmd: list[str], env: dict[str, str] | None = None) -> str:
    print(">>", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        print("STDOUT:", proc.stdout)
        print("STDERR:", proc.stderr)
        raise RuntimeError(f"Command failed with exit code {proc.returncode}: {cmd[0]}")
    return (proc.stdout or "") + (proc.stderr or "")


def build_apk() -> str:
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

    # 1. Sync latest frontend HTML into Android assets
    assets_dir = os.path.join(APP_MAIN, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    src_html = os.path.join(ROOT_DIR, "src", "frontend", "index.html")
    dst_html = os.path.join(assets_dir, "index.html")
    shutil.copy2(src_html, dst_html)
    print(f"[1/8] Synced {src_html} -> {dst_html} ({os.path.getsize(dst_html)} bytes)")

    # Prepare build subdirectories
    compiled_res_zip = os.path.join(BUILD_DIR, "compiled_res.zip")
    gen_java_dir = os.path.join(BUILD_DIR, "gen")
    classes_dir = os.path.join(BUILD_DIR, "classes")
    dex_dir = os.path.join(BUILD_DIR, "dex")
    os.makedirs(gen_java_dir, exist_ok=True)
    os.makedirs(classes_dir, exist_ok=True)
    os.makedirs(dex_dir, exist_ok=True)

    # 2. Compile resources via aapt2
    res_dir = os.path.join(APP_MAIN, "res")
    run_cmd([AAPT2, "compile", "--dir", res_dir, "-o", compiled_res_zip])
    print("[2/8] Compiled Android resources via aapt2")

    # 3. Link resources, AndroidManifest.xml, and assets via aapt2
    unsigned_unaligned_apk = os.path.join(BUILD_DIR, "tindawise-unaligned.apk")
    manifest_xml = os.path.join(APP_MAIN, "AndroidManifest.xml")
    run_cmd(
        [
            AAPT2,
            "link",
            "-o",
            unsigned_unaligned_apk,
            "-I",
            PLATFORM_JAR,
            "--manifest",
            manifest_xml,
            "-A",
            assets_dir,
            "--java",
            gen_java_dir,
            compiled_res_zip,
        ]
    )
    print("[3/8] Linked resources & assets into base APK and generated R.java")

    # 4. Compile Java sources (MainActivity.java + R.java) via javac
    main_java = os.path.join(APP_MAIN, "java", "ph", "edu", "batstateu", "tindawise", "MainActivity.java")
    r_java = os.path.join(gen_java_dir, "ph", "edu", "batstateu", "tindawise", "R.java")
    run_cmd(
        [
            JAVAC,
            "--release",
            "11",
            "-encoding",
            "UTF-8",
            "-cp",
            PLATFORM_JAR,
            "-d",
            classes_dir,
            main_java,
            r_java,
        ]
    )
    print("[4/8] Compiled Java sources to bytecode (.class)")

    # 5. Convert .class files to classes.dex via d8
    class_files: list[str] = []
    for root, _, files in os.walk(classes_dir):
        for fn in files:
            if fn.endswith(".class"):
                class_files.append(os.path.join(root, fn))

    env = os.environ.copy()
    env["JAVA_HOME"] = os.path.dirname(JBR_BIN)
    env["PATH"] = JBR_BIN + os.pathsep + env.get("PATH", "")

    run_cmd([D8, "--lib", PLATFORM_JAR, "--min-api", "24", "--output", dex_dir] + class_files, env=env)
    dex_file = os.path.join(dex_dir, "classes.dex")
    if not os.path.exists(dex_file):
        raise RuntimeError("d8 did not produce classes.dex")
    print(f"[5/8] Converted bytecode to {dex_file} ({os.path.getsize(dex_file)} bytes)")

    # 6. Add classes.dex to the APK archive
    with zipfile.ZipFile(unsigned_unaligned_apk, "a", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(dex_file, arcname="classes.dex")
    print("[6/8] Packaged classes.dex into APK")

    # 7. Align the APK via zipalign
    aligned_apk = os.path.join(BUILD_DIR, "tindawise-aligned.apk")
    run_cmd([ZIPALIGN, "-p", "-f", "4", unsigned_unaligned_apk, aligned_apk])
    print("[7/8] Aligned APK on 4-byte boundaries via zipalign")

    # 8. Generate signing key (if needed) and sign via apksigner
    keystore_path = os.path.join(ANDROID_DIR, "tindawise-release.jks")
    if not os.path.exists(keystore_path):
        run_cmd(
            [
                KEYTOOL,
                "-genkeypair",
                "-v",
                "-keystore",
                keystore_path,
                "-alias",
                "tindawise",
                "-keyalg",
                "RSA",
                "-keysize",
                "2048",
                "-validity",
                "10000",
                "-storepass",
                "tindawise2026",
                "-keypass",
                "tindawise2026",
                "-dname",
                "CN=TindaWise Team, OU=CICS, O=BatStateU The NEU, L=Batangas City, ST=Batangas, C=PH",
            ],
            env=env,
        )

    final_apk = os.path.join(DIST_DIR, "TindaWise-v1.0.0.apk")
    root_apk_copy = os.path.join(ROOT_DIR, "TindaWise-v1.0.0.apk")
    run_cmd(
        [
            APKSIGNER,
            "sign",
            "--ks",
            keystore_path,
            "--ks-key-alias",
            "tindawise",
            "--ks-pass",
            "pass:tindawise2026",
            "--key-pass",
            "pass:tindawise2026",
            "--out",
            final_apk,
            aligned_apk,
        ],
        env=env,
    )
    shutil.copy2(final_apk, root_apk_copy)
    print(f"[8/8] Signed APK created at:\n  - {final_apk}\n  - {root_apk_copy}")

    # Verify signature and badging
    verify_out = run_cmd([APKSIGNER, "verify", "--verbose", final_apk], env=env)
    print("\n=== APKSIGNER VERIFICATION ===")
    print(verify_out.strip())

    badging_out = run_cmd([AAPT2, "dump", "badging", final_apk], env=env)
    print("\n=== AAPT2 BADGING SUMMARY ===")
    for line in badging_out.splitlines()[:10]:
        print(line)

    return final_apk


if __name__ == "__main__":
    try:
        build_apk()
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(1)
