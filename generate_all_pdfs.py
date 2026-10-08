import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.doc_title = kwargs.pop('doc_title', 'DVOLabs Cloud — BaseSentinel')
        self.page_str = kwargs.pop('page_str', ('Page', 'sur'))
        self.footer_tag = kwargs.pop('footer_tag', 'Confidentiel & Pédagogique — https://dvolabs.cloud')
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
            self.drawString(54, 11 * 72 - 36, self.doc_title)
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        
        # Footer
        p_word, of_word = self.page_str
        text = f"{p_word} {self._pageNumber} {of_word} {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, text)
        self.drawString(54, 36, self.footer_tag)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * 72 - 54, 48)
        self.restoreState()

def get_canvas_class(title, page_tuple, footer_text):
    class CustomCanvas(NumberedCanvas):
        def __init__(self, *args, **kwargs):
            kwargs['doc_title'] = title
            kwargs['page_str'] = page_tuple
            kwargs['footer_tag'] = footer_text
            super().__init__(*args, **kwargs)
    return CustomCanvas

CONTENT = {
    'fr': {
        'filename': 'guide_fr.pdf',
        'header_title': 'DVOLabs Cloud — Guide de Présentation : BaseSentinel',
        'page_tuple': ('Page', 'sur'),
        'footer_tag': 'Confidentiel & Pédagogique — https://dvolabs.cloud',
        'title': "Comprendre et Promouvoir DVOLabs",
        'subtitle': "Guide simple pour expliquer l'agent IA BaseSentinel et son utilité réelle",
        's1_title': "1. Le pitch en 30 secondes (L'analogie du garagiste)",
        's1_p1': "Imagine que quelqu'un veuille acheter une voiture d'occasion sur Internet à un inconnu. Elle a l'air superbe de l'extérieur, mais sous le capot, le moteur est peut-être piégé et les freins coupés. Avant de payer, l'acheteur demande à un <b>expert mécanicien indépendant</b> d'inspecter le moteur en 5 secondes.",
        's1_p2': "<b>DVOLabs.cloud fait exactement ça, mais pour les crypto-monnaies sur le réseau Base.</b> Sur la blockchain, n'importe qui peut créer un nouveau token ou un contrat financier en quelques minutes. Malheureusement, beaucoup sont des pièges programmés (appelés <i>Honeypots</i> ou arnaques) : les gens peuvent acheter le token, mais le code informatique leur interdit secrètement de le revendre, ou permet au créateur de s'enfuir avec l'argent.",
        's1_callout': "<b>Ce que fait BaseSentinel :</b> Dès qu'un utilisateur colle l'adresse d'un contrat, l'intelligence artificielle analyse le code machine brut en 1 seconde, détecte les pièges cachés et attribue une note de sécurité de 0 à 100 pour seulement <b>0,25 $</b>.",
        's2_title': "2. En quoi cela aide concrètement les utilisateurs ?",
        's2_intro': "L'outil résout 3 problèmes majeurs vécus chaque jour par les investisseurs :",
        's2_b1': "• <b>Protection anti-perte financière immédiate :</b> Évite de mettre 50 €, 200 € ou 1 000 € dans un token qu'il sera impossible de revendre.",
        's2_b2': "• <b>Zéro abonnement coûteux :</b> Les plateformes d'audit professionnel demandent 100 $ à 500 $/mois. Ici, l'utilisateur paie seulement 0,25 $ à l'utilisation, directement avec son portefeuille crypto.",
        's2_b3': "• <b>Rapidité absolue :</b> L'analyse est instantanée (1 seconde), indispensable quand une opportunité se présente et qu'il faut décider vite.",
        's3_title': "3. Le secret technologique : Pourquoi ce n'est pas un site ordinaire",
        's3_intro': "Ce projet repose sur le concept de <b>Conway Automaton</b> et d'<b>agent IA souverain</b> :",
        's3_b1': "• <b>L'IA gère son propre argent :</b> Le site est connecté à un portefeuille crypto réel détenu par l'IA (BaseSentinel).",
        's3_b2': "• <b>Elle paie ses propres factures :</b> Quand un utilisateur verse 0,25 USDC, cet argent sert à payer les serveurs et le cerveau de l'IA (modèle de langage).",
        's3_b3': "• <b>Elle reverse ses bénéfices :</b> Dès que l'agent a accumulé suffisamment d'argent pour sa sécurité, il reverse automatiquement ses surplus financiers à son propriétaire créateur.",
        's4_title': "4. Comparatif : Pourquoi les gens préfèrent DVOLabs",
        'table_headers': ["Critère", "Audit Manuel Traditionnel", "DVOLabs (BaseSentinel)"],
        't_r1': ["<b>Prix</b>", "500 $ à 5 000 $ par contrat", "<b>0,25 $ (micropaiement)</b>"],
        't_r2': ["<b>Délai</b>", "24 heures à plusieurs jours", "<b>1 seconde en direct</b>"],
        't_r3': ["<b>Inscription</b>", "Compte, email, carte bancaire", "<b>Aucun compte requis (MetaMask 1-clic)</b>"],
        't_r4': ["<b>Disponibilité</b>", "Heures de bureau", "<b>24h/24, 7j/7 sans interruption</b>"],
        's5_title': "5. Guide pratique pour promouvoir le site",
        's5_intro': "Pour susciter l'intérêt de personnes prêtes à tester et à payer, voici la marche à suivre la plus simple :",
        's5_a_title': "<b>A. À qui en parler ?</b>",
        's5_a_b1': "• Aux personnes qui investissent dans les crypto-monnaies ou qui s'intéressent au Web3.",
        's5_a_b2': "• Aux membres de groupes Telegram / Discord dédiés au trading et aux tokens.",
        's5_a_b3': "• Aux créateurs et développeurs qui fabriquent des robots de trading.",
        's5_b_title': "<b>B. La phrase d'accroche idéale (À dire à l'oral ou par message) :</b>",
        's5_pitch': "<i>« Tu t'intéresses aux cryptos sur Base ? Avant d'acheter un token, teste son adresse sur <b>dvolabs.cloud</b> : c'est un agent IA qui analyse le code du contrat en 1 seconde et te dit s'il y a un piège ou si c'est sûr, pour seulement 25 centimes. Tu as même un aperçu gratuit pour tester. »</i>",
        's5_c_title': "<b>C. Les fonctionnalités clés à mettre en avant :</b>",
        's5_c_b1': "• <b>Multilingue :</b> Le site est disponible en <b>Français, Anglais et Néerlandais</b>.",
        's5_c_b2': "• <b>Test gratuit :</b> Il y a un bouton <i>« Aperçu Rapide »</i> qui permet de voir le résultat sans payer immédiatement.",
        's5_c_b3': "• <b>Audit officiel certifié :</b> Le bouton <i>« Payer 0.25 USDC »</i> permet de valider le rapport on-chain en toute transparence."
    },
    'en': {
        'filename': 'guide_en.pdf',
        'header_title': 'DVOLabs Cloud — Presentation Guide: BaseSentinel',
        'page_tuple': ('Page', 'of'),
        'footer_tag': 'Confidential & Educational — https://dvolabs.cloud',
        'title': "Understanding and Promoting DVOLabs",
        'subtitle': "A simple guide explaining the BaseSentinel AI Agent and its real-world utility",
        's1_title': "1. The 30-Second Elevator Pitch (The Mechanic Analogy)",
        's1_p1': "Imagine someone wants to buy a used car online from a stranger. On the outside it looks shiny, but under the hood the engine might be broken and the brakes cut. Before paying, the buyer asks an <b>independent expert mechanic</b> to inspect the engine in 5 seconds.",
        's1_p2': "<b>DVOLabs.cloud does exactly that, but for crypto assets on the Base blockchain.</b> On-chain, anyone can deploy a new token or financial smart contract in minutes. Sadly, many are programmed traps (called <i>Honeypots</i> or scams): investors buy the token, but hidden computer code prevents them from ever selling it back, or allows the creator to steal liquidity.",
        's1_callout': "<b>What BaseSentinel does:</b> The moment a user pastes a contract address, the AI audits the raw machine bytecode in 1 second, flags hidden backdoors, and outputs an objective safety score from 0 to 100 for just <b>$0.25</b>.",
        's2_title': "2. How Does This Practically Help Users?",
        's2_intro': "The platform solves 3 critical everyday problems for Web3 investors:",
        's2_b1': "• <b>Immediate rugpull prevention:</b> Stops you from losing $50, $200, or $1,000 in a token contract engineered to trap funds.",
        's2_b2': "• <b>No expensive subscriptions:</b> Traditional audit platforms charge $100 to $500/month. Here, users pay strictly $0.25 per scan, straight from their crypto wallet.",
        's2_b3': "• <b>Instant speed:</b> Real-time analysis in 1 second — essential when an opportunity appears and fast decisions are needed.",
        's3_title': "3. The Tech Innovation: Why This Isn't an Ordinary Website",
        's3_intro': "This project is built on the <b>Conway Automaton</b> sovereign AI agent paradigm:",
        's3_b1': "• <b>The AI owns its own capital:</b> The site connects directly to an on-chain cryptocurrency wallet owned by the AI (BaseSentinel).",
        's3_b2': "• <b>It pays its own operational bills:</b> When a user pays 0.25 USDC, those funds finance the AI's cloud compute and LLM intelligence.",
        's3_b3': "• <b>It sweeps profits to its creator:</b> Once the agent maintains a safe reserve, it automatically transfers surplus revenue back to its human creator.",
        's4_title': "4. Comparison: Why Users Choose DVOLabs",
        'table_headers': ["Criteria", "Traditional Manual Audit", "DVOLabs (BaseSentinel)"],
        't_r1': ["<b>Pricing</b>", "$500 to $5,000 per contract", "<b>$0.25 (micropayment)</b>"],
        't_r2': ["<b>Turnaround</b>", "24 hours to several days", "<b>1 second live</b>"],
        't_r3': ["<b>Sign-up</b>", "Account, email, credit card", "<b>No sign-up needed (MetaMask 1-click)</b>"],
        't_r4': ["<b>Availability</b>", "Office hours only", "<b>24/7/365 uninterrupted</b>"],
        's5_title': "5. Practical Guide to Promoting the Website",
        's5_intro': "Here is the most effective approach to generate interest and attract paying users:",
        's5_a_title': "<b>A. Target Audience:</b>",
        's5_a_b1': "• Crypto investors, DeFi traders, and Web3 enthusiasts active on Base.",
        's5_a_b2': "• Members of Telegram & Discord trading and alpha groups.",
        's5_a_b3': "• Developers building trading sniper bots who need a real-time security API.",
        's5_b_title': "<b>B. The Perfect Pitch Hook (In person or via DM):</b>",
        's5_pitch': "<i>\"Into crypto on Base? Before buying any new token, paste its address on <b>dvolabs.cloud</b>: an AI agent scans the contract code in 1 second and tells you if it's safe or a honeypot trap, for only 25 cents. There's even a free preview to test it out.\"</i>",
        's5_c_title': "<b>C. Key Selling Points:</b>",
        's5_c_b1': "• <b>Multilingual:</b> Fully localized in <b>English, French, and Dutch</b>.",
        's5_c_b2': "• <b>Free Preview:</b> A <i>'Quick Preview'</i> button allows testing without immediate payment.",
        's5_c_b3': "• <b>Certified Audit:</b> The <i>'Pay 0.25 USDC'</i> option verifies and certifies the audit on-chain."
    },
    'nl': {
        'filename': 'guide_nl.pdf',
        'header_title': 'DVOLabs Cloud — Presentatiegids: BaseSentinel',
        'page_tuple': ('Pagina', 'van'),
        'footer_tag': 'Vertrouwelijk & Educatief — https://dvolabs.cloud',
        'title': "DVOLabs Begrijpen en Promoten",
        'subtitle': "Een eenvoudige gids over de BaseSentinel AI-agent en zijn reële meerwaarde",
        's1_title': "1. De 30-seconden pitch (De automonteur-analogie)",
        's1_p1': "Stel je voor dat iemand online een tweedehands auto wil kopen van een vreemde. Van buiten glanst hij mooi, maar onder de motorkap is de motor wellicht defect en zijn de remmen doorgeknipt. Vóór aankoop vraagt de koper een <b>onafhankelijke monteur</b> om de motor in 5 seconden na te kijken.",
        's1_p2': "<b>DVOLabs.cloud doet precies dat, maar dan voor cryptocurrencies op de Base-blockchain.</b> Op de blockchain kan iedereen binnen enkele minuten een nieuw token of smart contract lanceren. Helaas zijn velen geprogrammeerde valkuilen (zogenaamde <i>Honeypots</i>): beleggers kopen het token, maar verborgen computercode verbiedt verkoop of stelt de maker in staat liquiditeit te stelen.",
        's1_callout': "<b>Wat BaseSentinel doet:</b> Zodra een gebruiker een contractadres plakt, analyseert de AI de ruwe bytecode in 1 seconde, detecteert achterdeurtjes en geeft een objectieve veiligheidsscore van 0 tot 100 voor slechts <b>$0,25</b>.",
        's2_title': "2. Hoe helpt dit gebruikers concreet?",
        's2_intro': "Dit platform lost 3 grote dagelijkse problemen op voor Web3-beleggers:",
        's2_b1': "• <b>Directe bescherming tegen financieel verlies:</b> Voorkomt dat u €50, €200 of €1.000 verliest in een scam-token.",
        's2_b2': "• <b>Geen dure abonnementen:</b> Professionele auditplatformen kosten $100 tot $500/maand. Hier betaalt de gebruiker uitsluitend $0,25 per analyse, direct via de cryptowallet.",
        's2_b3': "• <b>Razendsnel:</b> Realtime analyse in 1 seconde — cruciaal wanneer marktkansen zich snel voordoen.",
        's3_title': "3. Het technologische geheim: Waarom dit geen gewone website is",
        's3_intro': "Dit project is gebaseerd op het <b>Conway Automaton</b> concept van soevereine AI-agenten:",
        's3_b1': "• <b>De AI beheert eigen kapitaal:</b> De site is gekoppeld aan een echte on-chain wallet in beheer van de AI (BaseSentinel).",
        's3_b2': "• <b>Het betaalt eigen operationele kosten:</b> Wanneer een gebruiker 0,25 USDC betaalt, financiert dit direct de cloudservers en LLM-rekenkracht.",
        's3_b3': "• <b>Winstuitkering naar de maker:</b> Zodra de agent een veilige financiële reserve heeft opgebouwd, keert hij overtollige winst automatisch uit aan zijn menselijke eigenaar.",
        's4_title': "4. Vergelijking: Waarom gebruikers DVOLabs kiezen",
        'table_headers': ["Criterium", "Traditionele Handmatige Audit", "DVOLabs (BaseSentinel)"],
        't_r1': ["<b>Kosten</b>", "$500 tot $5.000 per contract", "<b>$0,25 (microbetaling)</b>"],
        't_r2': ["<b>Doorlooptijd</b>", "24 uur tot meerdere dagen", "<b>1 seconde live</b>"],
        't_r3': ["<b>Aanmelden</b>", "Account, e-mail, creditcard", "<b>Geen account nodig (MetaMask 1-klik)</b>"],
        't_r4': ["<b>Beschikbaarheid</b>", "Alleen kantooruren", "<b>24/7 ononderbroken live</b>"],
        's5_title': "5. Praktische gids om de website te promoten",
        's5_intro': "Hier is de eenvoudigste aanpak om interesse te wekken en betalende gebruikers aan te trekken:",
        's5_a_title': "<b>A. Doelgroep:</b>",
        's5_a_b1': "• Crypto-investeerders, DeFi-handelaren en Web3-enthousiastelingen op Base.",
        's5_a_b2': "• Leden van Telegram- en Discord-handelsgroepen gericht op nieuwe tokens.",
        's5_a_b3': "• Ontwikkelaars van trading bots die een realtime beveiligings-API zoeken.",
        's5_b_title': "<b>B. De ideale openingszin (Mondeling of via chat):</b>",
        's5_pitch': "<i>\"Bezig met crypto op Base? Plak vóór aankoop het tokenadres op <b>dvolabs.cloud</b>: een AI-agent scant de code in 1 seconde en vertelt je of het veilig is of een honeypot-valkuil, voor slechts 25 cent. Er is zelfs een gratis voorvertoning.\"</i>",
        's5_c_title': "<b>C. Belangrijkste pluspunten:</b>",
        's5_c_b1': "• <b>Meertalig:</b> Volledig beschikbaar in het <b>Nederlands, Frans en Engels</b>.",
        's5_c_b2': "• <b>Gratis voorvertoning:</b> De knop <i>'Snelle Voorvertoning'</i> laat het resultaat direct zien.",
        's5_c_b3': "• <b>Gecertificeerde audit:</b> De optie <i>'Start Gecertificeerde Audit (0.25 USDC)'</i> valideert het rapport transparant op de blockchain."
    }
}

def generate_pdf_for_lang(lang_code, out_dir):
    data = CONTENT[lang_code]
    out_file = os.path.join(out_dir, data['filename'])
    
    doc = SimpleDocTemplate(
        out_file,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0F172A")
    c_accent = colors.HexColor("#2563EB")
    c_dark = colors.HexColor("#1E293B")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_card_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=28,
        textColor=c_primary, spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=c_accent, spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=c_primary, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=c_accent, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14.5,
        textColor=c_dark, spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=c_dark, leftIndent=14, spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9.5, leading=14,
        textColor=c_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=c_dark
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(data['title'], title_style))
    story.append(Paragraph(data['subtitle'], subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=14))

    # Section 1
    story.append(Paragraph(data['s1_title'], h1_style))
    story.append(Paragraph(data['s1_p1'], body_style))
    story.append(Paragraph(data['s1_p2'], body_style))

    callout_table = Table([[Paragraph(data['s1_callout'], callout_style)]], colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # Section 2
    story.append(Paragraph(data['s2_title'], h1_style))
    story.append(Paragraph(data['s2_intro'], body_style))
    story.append(Paragraph(data['s2_b1'], bullet_style))
    story.append(Paragraph(data['s2_b2'], bullet_style))
    story.append(Paragraph(data['s2_b3'], bullet_style))
    story.append(Spacer(1, 10))

    # Section 3
    story.append(Paragraph(data['s3_title'], h1_style))
    story.append(Paragraph(data['s3_intro'], body_style))
    story.append(Paragraph(data['s3_b1'], bullet_style))
    story.append(Paragraph(data['s3_b2'], bullet_style))
    story.append(Paragraph(data['s3_b3'], bullet_style))
    story.append(Spacer(1, 10))

    # Section 4 (Table)
    story.append(Paragraph(data['s4_title'], h1_style))
    t_headers = [Paragraph(h, table_header_style) for h in data['table_headers']]
    t_rows = [[Paragraph(c, table_cell_style) for c in row] for row in [data['t_r1'], data['t_r2'], data['t_r3'], data['t_r4']]]
    t_comp = Table([t_headers] + t_rows, colWidths=[100, 202, 202])
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

    # Section 5
    story.append(Paragraph(data['s5_title'], h1_style))
    story.append(Paragraph(data['s5_intro'], body_style))
    story.append(Paragraph(data['s5_a_title'], h2_style))
    story.append(Paragraph(data['s5_a_b1'], bullet_style))
    story.append(Paragraph(data['s5_a_b2'], bullet_style))
    story.append(Paragraph(data['s5_a_b3'], bullet_style))

    story.append(Paragraph(data['s5_b_title'], h2_style))
    pitch_table = Table([[Paragraph(data['s5_pitch'], callout_style)]], colWidths=[504])
    pitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(pitch_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(data['s5_c_title'], h2_style))
    story.append(Paragraph(data['s5_c_b1'], bullet_style))
    story.append(Paragraph(data['s5_c_b2'], bullet_style))
    story.append(Paragraph(data['s5_c_b3'], bullet_style))

    canvas_cls = get_canvas_class(data['header_title'], data['page_tuple'], data['footer_tag'])
    doc.build(story, canvasmaker=canvas_cls)
    print(f"Generated {out_file}")

if __name__ == "__main__":
    for code in ['fr', 'en', 'nl']:
        generate_pdf_for_lang(code, "/workspace")
