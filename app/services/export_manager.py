import csv
import io
import json
from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

from app.models import Comment


class ExportStrategy(ABC):
    """Abstract Strategy class for data export."""
    @abstractmethod
    def export(self, posts):
        pass


class CSVExportStrategy(ExportStrategy):
    """Strategy for exporting posts into CSV format."""
    def export(self, posts):
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ID', 'Author', 'Timestamp', 'Body'])

        for post in posts:
            writer.writerow([
                post.id,
                post.author.username if post.author else 'Unknown',
                post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                post.body
            ])
        return output.getvalue().encode('utf-8')


class JSONExportStrategy(ExportStrategy):
    """Strategy for exporting posts into JSON format with nested comments for single post."""
    def export(self, posts):
        data = []
        is_single_post = len(posts) == 1

        for post in posts:
            post_data = {
                'id': post.id,
                'author': post.author.username if post.author else 'Unknown',
                'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'body': post.body
            }

            if is_single_post:
                comments_list = []
                for comment in post.comments.order_by(Comment.timestamp.asc()):
                    if comment.disabled:
                        continue
                    comments_list.append({
                        'id': comment.id,
                        'author': comment.author.username if comment.author else 'Unknown',
                        'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'body': comment.body
                    })
                post_data['comments'] = comments_list

            data.append(post_data)

        return json.dumps(data, ensure_ascii=False, indent=4).encode('utf-8')


class PDFExportStrategy(ExportStrategy):
    """Strategy for exporting posts into PDF format with Cyrillic support."""
    def export(self, posts):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

        try:
            font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
            pdfmetrics.registerFont(TTFont('Arial-UA', font_path))
            font_name = 'Arial-UA'
        except Exception:
            font_name = 'Helvetica'

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'PDFTitle', parent=styles['Heading1'], fontName=font_name, fontSize=18, spaceAfter=20
        )
        meta_style = ParagraphStyle(
            'PDFMeta', parent=styles['Normal'], fontName=font_name, fontSize=9, textColor='gray', spaceAfter=4
        )
        body_style = ParagraphStyle(
            'PDFBody', parent=styles['Normal'], fontName=font_name, fontSize=11, spaceAfter=12
        )
        comment_meta_style = ParagraphStyle(
            'PDFCommentMeta', parent=styles['Normal'], fontName=font_name, fontSize=8, textColor='darkred',
            leftIndent=20, spaceAfter=2
        )
        comment_body_style = ParagraphStyle(
            'PDFCommentBody', parent=styles['Normal'], fontName=font_name, fontSize=9.5, leftIndent=20, spaceAfter=8
        )

        is_single_post = len(posts) == 1
        title_text = f"Export of Post #{posts[0].id}" if is_single_post else "Export of Flasky Feed"

        story = [Paragraph(title_text, title_style), Spacer(1, 10)]

        for post in posts:
            author = post.author.username if post.author else 'Unknown'
            date = post.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            clean_body = post.body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

            meta_text = f"<b>Post #{post.id}</b> | Author: {author} | Date: {date}"
            story.append(Paragraph(meta_text, meta_style))
            story.append(Paragraph(clean_body, body_style))

            if is_single_post and post.comments.count() > 0:
                story.append(Paragraph("<b>Comments:</b>", comment_body_style))
                for comment in post.comments.order_by(Comment.timestamp.asc()):
                    if comment.disabled:
                        continue
                    c_author = comment.author.username if comment.author else 'Unknown'
                    c_date = comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    c_clean = comment.body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                    c_meta = f"From: {c_author} | Date: {c_date}"
                    story.append(Paragraph(c_meta, comment_meta_style))
                    story.append(Paragraph(c_clean, comment_body_style))

            story.append(Paragraph(
                "<font color='lightgrey'>__________________________________________________________________</font>",
                body_style))
            story.append(Spacer(1, 10))

        doc.build(story)
        return buffer.getvalue()


class ExportContext:
    """Context class that manages the active ExportStrategy."""
    def __init__(self, strategy: ExportStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ExportStrategy):
        self._strategy = strategy

    def execute_export(self, posts):
        return self._strategy.export(posts)