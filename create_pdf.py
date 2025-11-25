# save as: create_biogas_substrates_pdf.py
from xml.etree import ElementTree as ET
from datetime import datetime
from fpdf import FPDF

# ============== ENGLISH TRANSLATION DICTIONARY ==============
translation = {
    "Silomais": "Maize silage",
    "Gülle": "Pig manure",
    "Grünroggen": "Green rye",
    "Grassilage": "Grass silage",
    "Getreide": "Grain (whole crop)",
    "GPS": "Whole crop silage (GPS)",
    "CCM": "Corn-Cob-Mix (CCM)",
    "Futterkalk": "Feed lime (CaCO3)",
    "Rindermist": "Cattle solid manure",
    "Zwiebeln": "Onions",
    
    # classes
    "Mais (GPS) (EK I)": "Maize (WCS) (renewable raw materials class I)",
    "Schweinegülle (EK II)": "Pig manure (manure class II)",
    "Grünroggen (GPS) (EK I)": "Green rye (WCS) (class I)",
    "Gras/Ackergras (EK I)": "Grass/permanent grassland (class I)",
    "Getreide (GPS) (EK I)": "Grain (WCS) (class I)",
    "Corn-Cob-Mix (CCM) (EK I)": "Corn-Cob-Mix (CCM) (class I)",
    "Miscellaneous": "Miscellaneous",
    "Rinderfestmist (EK II)": "Cattle solid manure (class II)",
    "Sonstiges (EK 0)": "Others (class 0)",

    # labels (German → English)
    "raw fiber (Rohfaser)": "Crude fibre (XF)",
    "raw protein (Rohprotein)": "Crude protein (XP)",
    "raw lipids (Rohfett)": "Crude fat (XL)",
    "neutral detergent fiber": "Neutral detergent fibre (NDF)",
    "acid detergent fiber": "Acid detergent fibre (ADF)",
    "acid detergent lignin": "Acid detergent lignin (ADL)",
    
    "total solids (VS + Ash)": "Total solids (TS)",
    "volatile solids (sum of all COD containing components)": "Volatile solids (VS)",
    "degradation level": "Degree of degradation (VS degradation)",
    "disintegration rate": "Disintegration rate constant k_dis",
    "hydrolysis rate carbohydrates": "Carbohydrate hydrolysis rate k_hyd_ch",
    "hydrolysis rate proteins": "Protein hydrolysis rate k_hyd_pr",
    "hydrolysis rate lipids": "Lipid hydrolysis rate k_hyd_li",
    "cost": "Substrate cost",
}

class BiogasPDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, 'Biogas Substrates – Detailed Parameter Set (English)', ln=1, align='C')
        self.set_font('DejaVu', '', 10)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# Load XML
tree = ET.parse('substrate_gummersbach.xml')
root = tree.getroot()

pdf = BiogasPDF()
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # you need this font or replace with Arial
pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

for substrate in root.findall('substrate'):
    sub_id = substrate.get('id')
    name_de = substrate.find('name').text
    name_en = translation.get(name_de, name_de)
    
    pdf.set_font('DejaVu', 'B', 14)
    pdf.set_fill_color(230, 230, 250)
    pdf.cell(0, 10, f"{name_en} ({sub_id})", ln=1, fill=True)
    
    cls = substrate.find('substrate_class').text
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 8, f"Class: {translation.get(cls, cls)}", ln=1)
    
    cost = substrate.find("./physValue[@symbol='cost']").find('value').text
    unit = substrate.find("./physValue[@symbol='cost']").find('unit').text
    pdf.cell(0, 8, f"Cost: {cost} {unit}", ln=1)
    pdf.ln(4)

    # Weender analysis
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 8, "Weender analysis (% of TS)", ln=1)
    pdf.set_font('DejaVu', '', 10)
    for sym in ["RF", "RP", "RL", "NDF", "ADF", "ADL"]:
        el = substrate.find(f".//Weender/physValue[@symbol='{sym}']")
        if el is not None:
            val = el.find('value').text
            unit = el.find('unit').text
            label = el.find('label').text
            label_en = translation.get(label, label)
            ref = el.find('reference').text if el.find('reference') is not None else ""
            pdf.set_font('DejaVu', '', 10)
            pdf.multi_cell(0, 6, f"• {label_en}: {val} {unit}")
            if ref.strip():
                pdf.set_font('DejaVu', 'I', 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(0, 5, f"   Ref: {ref}")
                pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Physical & chemical parameters
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 8, "Physical & Chemical Parameters", ln=1)
    pdf.set_font('DejaVu', '', 10)
    phys_symbols = ["TS", "VS", "pH", "Sac", "Spro", "Sbu", "Sva", "Snh4", "TAC", "T", "D_VS", "COD_S", "SIin"]
    for sym in phys_symbols:
        el = substrate.find(f".//Phys/physValue[@symbol='{sym}']")
        if el is not None:
            val = el.find('value').text
            unit = el.find('unit').text
            label = el.find('label').text
            label_en = translation.get(label, label)
            ref = el.find('reference').text if el.find('reference') is not None else ""
            pdf.multi_cell(0, 6, f"• {label_en}: {val} {unit}")
            if ref.strip():
                pdf.set_font('DejaVu', 'I', 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(0, 5, f"   Ref: {ref}")
                pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # ADM1 kinetic parameters
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 8, "Anaerobic Digestion Model No.1 (ADM1) Kinetic Parameters", ln=1)
    pdf.set_font('DejaVu', '', 10)
    for sym in ["kdis", "khyd_ch", "khyd_pr", "khyd_li", "km_c4", "km_pro", "km_ac", "km_h2"]:
        el = substrate.find(f".//AD/physValue[@symbol='{sym}']")
        if el is not None:
            val = el.find('value').text
            unit = el.find('unit').text
            label = el.find('label').text if el.find('label') is not None else sym
            label_en = translation.get(label, label)
            ref = el.find('reference').text if el.find('reference') is not None else ""
            pdf.multi_cell(0, 6, f"• {translation.get(label_en, label_en)}: {val} {unit}")
            if ref.strip():
                pdf.set_font('DejaVu', 'I', 9)
                pdf.multi_cell(0, 5, f"   Ref: {ref}")
    pdf.ln(15)

pdf.output("Biogas_Substrates_Gummersbach_ENGLISH.pdf")
print("PDF successfully created: Biogas_Substrates_Gummersbach_ENGLISH.pdf")