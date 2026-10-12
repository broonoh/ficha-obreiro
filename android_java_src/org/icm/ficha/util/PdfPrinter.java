package org.icm.ficha.util;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Rect;
import android.graphics.pdf.PdfDocument;
import android.view.View;
import android.webkit.WebView;

import java.io.File;
import java.io.FileOutputStream;

/**
 * Gera um PDF de verdade a partir de um WebView, sem depender da UI de
 * impressão do sistema Android.
 *
 * A API pública de impressão do Android (PrintDocumentAdapter.onLayout /
 * onWrite) exige instâncias de LayoutResultCallback/WriteResultCallback
 * cujo construtor é propositalmente não-público fora do pacote
 * android.print — ou seja, só o próprio spooler de impressão do sistema
 * pode dirigir esse fluxo, e ele sempre aparece como uma tela para o
 * usuário escolher "onde salvar". Para gerar o arquivo direto (sem essa
 * tela) e já abrir o compartilhamento nativo em seguida, renderizamos o
 * conteúdo do WebView inteiro num Bitmap e montamos as páginas do PDF nós
 * mesmos com PdfDocument — mesma técnica usada por apps de "exportar tela
 * como PDF".
 */
public class PdfPrinter {

    public interface Callback {
        void onSuccess();
        void onError(String message);
    }

    // Página A4 em pontos (1/72 polegada) — unidade nativa do PdfDocument.
    private static final int PAGE_WIDTH_PT = 595;
    private static final int PAGE_HEIGHT_PT = 842;
    // Fator de escala pra renderizar em resolução maior que o PDF final,
    // mantendo o texto nítido depois de reamostrado para baixo.
    private static final int SCALE = 2;

    public static void printToFile(WebView webView, String outputPath, Callback callback) {
        Bitmap bitmap = null;
        PdfDocument document = null;
        try {
            int widthPx = PAGE_WIDTH_PT * SCALE;

            webView.measure(
                    View.MeasureSpec.makeMeasureSpec(widthPx, View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED));

            int contentHeightPx = webView.getContentHeight() * SCALE;
            if (contentHeightPx <= 0) {
                contentHeightPx = PAGE_HEIGHT_PT * SCALE;
            }
            webView.layout(0, 0, widthPx, contentHeightPx);

            bitmap = Bitmap.createBitmap(widthPx, contentHeightPx, Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(bitmap);
            canvas.drawColor(Color.WHITE);
            webView.draw(canvas);

            int pageHeightPx = PAGE_HEIGHT_PT * SCALE;
            int totalPages = (int) Math.ceil(contentHeightPx / (double) pageHeightPx);
            if (totalPages <= 0) {
                totalPages = 1;
            }

            document = new PdfDocument();
            for (int i = 0; i < totalPages; i++) {
                PdfDocument.PageInfo pageInfo =
                        new PdfDocument.PageInfo.Builder(PAGE_WIDTH_PT, PAGE_HEIGHT_PT, i + 1).create();
                PdfDocument.Page page = document.startPage(pageInfo);

                int srcTop = i * pageHeightPx;
                int srcBottom = Math.min(srcTop + pageHeightPx, contentHeightPx);
                Rect src = new Rect(0, srcTop, widthPx, srcBottom);
                int dstHeight = Math.round((srcBottom - srcTop) / (float) SCALE);
                Rect dst = new Rect(0, 0, PAGE_WIDTH_PT, dstHeight);

                page.getCanvas().drawBitmap(bitmap, src, dst, null);
                document.finishPage(page);
            }

            File outFile = new File(outputPath);
            FileOutputStream out = new FileOutputStream(outFile);
            document.writeTo(out);
            out.close();

            callback.onSuccess();
        } catch (Exception e) {
            callback.onError(e.getMessage());
        } finally {
            if (document != null) {
                document.close();
            }
            if (bitmap != null) {
                bitmap.recycle();
            }
        }
    }
}
