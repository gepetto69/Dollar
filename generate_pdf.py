import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "DVOLabs Cloud — Guide de Présentation : BaseSentinel")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        
        # Footer
        text = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, text)
        self.drawString(54, 36, "Confidentiel & Pédagogique — https://dvolabs.cloud")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * 72 - 54, 48)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Navy
    c_accent = colors.HexColor("#2563EB")     # Electric Blue
    c_secondary = colors.HexColor("#475569")  # Slate Gray
    c_dark = colors.HexColor("#1E293B")       # Dark Charcoal
    c_bg_light = colors.HexColor("#F8FAFC")   # Light gray for callouts
    c_card_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        leftIndent=14,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1E293B")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    story = []

    # Title Banner
    story.append(Paragraph("Comprendre et Promouvoir DVOLabs", title_style))
    story.append(Paragraph("Guide simple pour expliquer l'agent IA BaseSentinel et son utilité réelle", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=14))

    # Introduction / Pitch en 30 secondes
    story.append(Paragraph("1. Le pitch en 30 secondes (L'analogie du garagiste)", h1_style))
    story.append(Paragraph(
        "Imagine que quelqu'un veuille acheter une voiture d'occasion sur Internet à un inconnu. "
        "Elle a l'air superbe de l'extérieur, mais sous le capot, le moteur est peut-être piégé et les freins coupés. "
        "Avant de payer, l'acheteur demande à un <b>expert mécanicien indépendant</b> d'inspecter le moteur en 5 secondes.",
        body_style
    ))
    story.append(Paragraph(
        "<b>DVOLabs.cloud fait exactement ça, mais pour les crypto-monnaies sur le réseau Base.</b> "
        "Sur la blockchain, n'importe qui peut créer un nouveau token ou un contrat financier en quelques minutes. "
        "Malheureusement, beaucoup sont des pièges programmés (appelés <i>Honeypots</i> ou arnaques) : les gens peuvent acheter le token, "
        "mais le code informatique leur interdit secrètement de le revendre, ou permet au créateur de s'enfuir avec l'argent.",
        body_style
    ))

    # Box analogie
    callout_data = [[
        Paragraph(
            "<b>Ce que fait BaseSentinel :</b> Dès qu'un utilisateur colle l'adresse d'un contrat, l'intelligence artificielle analyse le code machine brut en 1 seconde, détecte les pièges cachés et attribue une note de sécurité de 0 à 100 pour seulement <b>0,25 $</b>.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # 2. En quoi ça aide les utilisateurs ?
    story.append(Paragraph("2. En quoi cela aide concrètement les utilisateurs ?", h1_style))
    story.append(Paragraph("L'outil résout 3 problèmes majeurs vécus chaque jour par les investisseurs :", body_style))
    story.append(Paragraph("• <b>Protection anti-perte financière immédiate :</b> Évite de mettre 50 €, 200 € ou 1 000 € dans un token qu'il sera impossible de revendre.", bullet_style))
    story.append(Paragraph("• <b>Zéro abonnement coûteux :</b> Les plateformes d'audit professionnel demandent 100 $ à 500 $/mois. Ici, l'utilisateur paie seulement 0,25 $ à l'utilisation, directement avec son portefeuille crypto.", bullet_style))
    story.append(Paragraph("• <b>Rapidité absolue :</b> L'analyse est instantanée (1 seconde), indispensable quand une opportunité se présente et qu'il faut décider vite.", bullet_style))
    story.append(Spacer(1, 10))

    # 3. Le concept révolutionnaire d'Agent IA Autonome
    story.append(Paragraph("3. Le secret technologique : Pourquoi ce n'est pas un site ordinaire", h1_style))
    story.append(Paragraph(
        "Ce projet repose sur le concept de <b>Conway Automaton</b> et d'<b>agent IA souverain</b> :",
        body_style
    ))
    story.append(Paragraph("• <b>L'IA gère son propre argent :</b> Le site est connecté à un portefeuille crypto réel détenu par l'IA (BaseSentinel).", bullet_style))
    story.append(Paragraph("• <b>Elle paie ses propres factures :</b> Quand un utilisateur verse 0,25 USDC, cet argent sert à payer les serveurs et le cerveau de l'IA (modèle de langage).", bullet_style))
    story.append(Paragraph("• <b>Elle reverse ses bénéfices :</b> Dès que l'agent a accumulé suffisamment d'argent pour sa sécurité, il reverse automatiquement ses surplus financiers à son propriétaire créateur.", bullet_style))
    story.append(Spacer(1, 10))

    # 4. Tableau comparatif
    story.append(Paragraph("4. Comparatif : Pourquoi les gens préfèrent DVOLabs", h1_style))
    table_data = [
        [
            Paragraph("Critère", table_header_style),
            Paragraph("Audit Manuel Traditionnel", table_header_style),
            Paragraph("DVOLabs (BaseSentinel)", table_header_style)
        ],
        [
            Paragraph("<b>Prix</b>", table_cell_style),
            Paragraph("500 $ à 5 000 $ par contrat", table_cell_style),
            Paragraph("<b>0,25 $ (micropaiement)</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Délai</b>", table_cell_style),
            Paragraph("24 heures à plusieurs jours", table_cell_style),
            Paragraph("<b>1 seconde en direct</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Inscription</b>", table_cell_style),
            Paragraph("Compte, email, carte bancaire", table_cell_style),
            Paragraph("<b>Aucun compte requis (MetaMask 1-clic)</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Disponibilité</b>", table_cell_style),
            Paragraph("Heures de bureau", table_cell_style),
            Paragraph("<b>24h/24, 7j/7 sans interruption</b>", table_cell_style)
        ]
    ]
    t_comp = Table(table_data, colWidths=[100, 202, 202])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, c_card_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 12))

    # 5. Comment ton fils peut le promouvoir facilement
    story.append(Paragraph("5. Guide pratique pour promouvoir le site", h1_style))
    story.append(Paragraph(
        "Pour susciter l'intérêt de personnes prêtes à tester et à payer, voici la marche à suivre la plus simple :",
        body_style
    ))
    
    story.append(Paragraph("<b>A. À qui en parler ?</b>", h2_style))
    story.append(Paragraph("• Aux personnes qui investissent dans les crypto-monnaies ou qui s'intéressent au Web3.", bullet_style))
    story.append(Paragraph("• Aux membres de groupes Telegram / Discord dédiés au trading et aux tokens.", bullet_style))
    story.append(Paragraph("• Aux créateurs et développeurs qui fabriquent des robots de trading.", bullet_style))

    story.append(Paragraph("<b>B. La phrase d'accroche idéale (À dire à l'oral ou par message) :</b>", h2_style))
    
    pitch_box = [[
        Paragraph(
            "<i>« Tu t'intéresses aux cryptos sur Base ? Avant d'acheter un token, teste son adresse sur <b>dvolabs.cloud</b> : c'est un agent IA qui analyse le code du contrat en 1 seconde et te dit s'il y a un piège ou si c'est sûr, pour seulement 25 centimes. Tu as même un aperçu gratuit pour tester. »</i>",
            callout_style
        )
    ]]
    t_pitch = Table(pitch_box, colWidths=[504])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>C. Les fonctionnalités clés à mettre en avant :</b>", h2_style))
    story.append(Paragraph("• <b>Multilingue :</b> Le site est disponible en <b>Français, Anglais et Néerlandais</b>.", bullet_style))
    story.append(Paragraph("• <b>Test gratuit :</b> Il y a un bouton <i>« Aperçu Rapide »</i> qui permet de voir le résultat sans payer immédiatement.", bullet_style))
    story.append(Paragraph("• <b>Audit officiel certifié :</b> Le bouton <i>« Payer 0.25 USDC »</i> permet de valider le rapport on-chain en toute transparence.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at {filename}")

if __name__ == "__main__":
    out_path = "/workspace/GUIDE_PROMOTION_DVOLABS.pdf"
    build_pdf(out_path)
