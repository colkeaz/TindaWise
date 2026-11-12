package ph.edu.batstateu.tindawise;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.util.ArrayList;

/**
 * TindaWise Android Native Container & Ephemeral Speech / Manual Reminder Bridge.
 *
 * Guarantees:
 * 1. Push-to-Talk Speech Recognition uses Android's native RecognizerIntent (fil-PH / Taglish)
 *    with zero audio files written to storage (RA 10173 0-day audio retention).
 * 2. LocalStorage is enabled so the Owner-Editable Price List and Deterministic Utang Ledger
 *    persist locally on the store owner's device.
 * 3. Reminders are opened in the owner's native SMS or Messenger app for manual sending.
 */
public class MainActivity extends Activity {

    private static final int REQ_SPEECH_RECOGNIZER = 1001;
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        WebView.setWebContentsDebuggingEnabled(true);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.addJavascriptInterface(new AndroidBridge(this), "AndroidBridge");

        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_SPEECH_RECOGNIZER) {
            String spoken = "";
            if (resultCode == RESULT_OK && data != null) {
                ArrayList<String> matches = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                if (matches != null && !matches.isEmpty()) {
                    spoken = matches.get(0);
                }
            }
            final String escaped = spoken
                    .replace("\\", "\\\\")
                    .replace("\"", "\\\"")
                    .replace("\n", " ")
                    .replace("\r", " ");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    webView.evaluateJavascript(
                            "window.onAndroidSpeechResult && window.onAndroidSpeechResult(\"" + escaped + "\");",
                            null
                    );
                }
            });
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    public class AndroidBridge {
        private final Context context;

        public AndroidBridge(Context ctx) {
            this.context = ctx;
        }

        @JavascriptInterface
        public void startVoiceRecognition() {
            try {
                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "fil-PH");
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "fil-PH");
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Magsalita ng Taglish Utang (hal. Palista kay Aling Nena...)");
                startActivityForResult(intent, REQ_SPEECH_RECOGNIZER);
            } catch (Exception e) {
                Toast.makeText(context, "Voice recognizer unavailable; using Tap Fallback.", Toast.LENGTH_SHORT).show();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        webView.evaluateJavascript(
                                "window.onAndroidSpeechResult && window.onAndroidSpeechResult(\"\");",
                                null
                        );
                    }
                });
            }
        }

        @JavascriptInterface
        public void openSmsComposer(String phone, String message) {
            try {
                String cleanPhone = phone != null ? phone.trim() : "";
                Uri uri = cleanPhone.isEmpty() ? Uri.parse("sms:") : Uri.parse("smsto:" + Uri.encode(cleanPhone));
                Intent smsIntent = new Intent(Intent.ACTION_SENDTO, uri);
                smsIntent.putExtra("sms_body", message);
                smsIntent.putExtra(Intent.EXTRA_TEXT, message);
                smsIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(smsIntent);
            } catch (Exception e) {
                try {
                    String cleanPhone = phone != null ? phone.trim() : "";
                    Intent viewIntent = new Intent(Intent.ACTION_VIEW);
                    viewIntent.setData(cleanPhone.isEmpty() ? Uri.parse("sms:") : Uri.parse("sms:" + Uri.encode(cleanPhone)));
                    viewIntent.putExtra("sms_body", message);
                    viewIntent.putExtra(Intent.EXTRA_TEXT, message);
                    viewIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    context.startActivity(viewIntent);
                } catch (Exception e2) {
                    Toast.makeText(context, "Could not open SMS app. Text copied instead.", Toast.LENGTH_SHORT).show();
                    copyToClipboard(message);
                }
            }
        }

        @JavascriptInterface
        public void shareReminder(String message) {
            try {
                Intent shareIntent = new Intent(Intent.ACTION_SEND);
                shareIntent.setType("text/plain");
                shareIntent.putExtra(Intent.EXTRA_TEXT, message);
                shareIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(Intent.createChooser(shareIntent, "Send Utang Reminder via..."));
            } catch (Exception e) {
                copyToClipboard(message);
            }
        }

        @JavascriptInterface
        public void copyToClipboard(String text) {
            ClipboardManager clipboard = (ClipboardManager) context.getSystemService(Context.CLIPBOARD_SERVICE);
            if (clipboard != null) {
                ClipData clip = ClipData.newPlainText("TindaWise Reminder", text);
                clipboard.setPrimaryClip(clip);
                Toast.makeText(context, "Reminder copied to clipboard!", Toast.LENGTH_SHORT).show();
            }
        }

        @JavascriptInterface
        public void showToast(String message) {
            Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
        }
    }
}
