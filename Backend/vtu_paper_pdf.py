import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_vtu_paper_pdf(paper_data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'VTUTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#0f172a')
    )
    
    sub_title_style = ParagraphStyle(
        'VTUSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#1e293b')
    )
    
    header_meta_style = ParagraphStyle(
        'VTUMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    
    note_style = ParagraphStyle(
        'VTUNote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )
    
    q_cell_style = ParagraphStyle(
        'VTUQCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )
    
    th_style = ParagraphStyle(
        'VTUTh',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#ffffff')
    )
    
    or_style = ParagraphStyle(
        'VTUOr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#dc2626')
    )

    story = []

    # 1. USN BOX TABLE
    usn_boxes = '  '.join(['[  ]' for _ in range(10)])
    course_c = paper_data.get('course_code', '22CS34')
    usn_data = [
        [Paragraph('<b>USN</b>', header_meta_style), Paragraph(f'<b>{usn_boxes}</b>', header_meta_style), Paragraph(f'<b>{course_c}</b>', ParagraphStyle('R', parent=header_meta_style, alignment=2))]
    ]
    usn_table = Table(usn_data, colWidths=[40, 360, 120])
    usn_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(usn_table)
    story.append(Spacer(1, 6))

    # 2. UNIVERSITY HEADER
    univ_name = paper_data.get('university', 'VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI')
    scheme = paper_data.get('scheme', '2022')
    sem = paper_data.get('semester', '3')
    branch = paper_data.get('branch', 'Computer Science & Engineering')
    subject = paper_data.get('subject', 'Data Structures and Applications')
    code = paper_data.get('course_code', '22CS34')
    
    story.append(Paragraph(univ_name, title_style))
    story.append(Paragraph(f'<b>Model Question Paper ({scheme} Scheme) with effect from {scheme}</b>', sub_title_style))
    story.append(Paragraph(f'<b>{sem}th Semester B.E. / B.Tech. Degree Examination</b>', sub_title_style))
    story.append(Paragraph(f'<b>Course Title: {subject} ({branch})</b>', sub_title_style))
    story.append(Spacer(1, 6))

    # 3. EXAM META
    meta_data = [
        [
            Paragraph('<b>Time: 3 Hours</b>', header_meta_style),
            Paragraph(f'<b>Course Code: {code}</b>', ParagraphStyle('C', parent=header_meta_style, alignment=1)),
            Paragraph('<b>Max. Marks: 100</b>', ParagraphStyle('R', parent=header_meta_style, alignment=2))
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 180, 170])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#0f172a')),
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#0f172a')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # 4. INSTRUCTIONS
    story.append(Paragraph('<b>Note:</b> 1. Answer any <b>FIVE</b> full questions, choosing <b>ONE</b> full question from each module.', note_style))
    story.append(Paragraph('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. <b>M:</b> Marks, <b>L:</b> Revised Bloom\'s Taxonomy Level (L1: Remember, L2: Understand, L3: Apply, L4: Analyze), <b>CO:</b> Course Outcome.', note_style))
    story.append(Spacer(1, 6))

    # 5. QUESTION TABLE
    table_rows = [
        [
            Paragraph('<b>Module</b>', th_style),
            Paragraph('<b>Q.No.</b>', th_style),
            Paragraph('<b>Question Description</b>', th_style),
            Paragraph('<b>Marks</b>', th_style),
            Paragraph('<b>Level</b>', th_style),
            Paragraph('<b>CO</b>', th_style)
        ]
    ]

    tstyles = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('ALIGN', (0,0), (1,-1), 'CENTER'),
        ('ALIGN', (3,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]

    curr_row = 1
    modules = paper_data.get('modules', [])

    for m in modules:
        mod_num = m.get('module_num', 1)
        co_tag = m.get('co', f'CO{mod_num}')
        
        # Question Odd
        q_odd = m.get('question_odd', {})
        q_odd_num = q_odd.get('q_num', (mod_num-1)*2 + 1)
        parts_odd = q_odd.get('parts', [])
        
        for idx, p in enumerate(parts_odd):
            sub_lbl = p.get('sub_q', 'a')
            q_num_disp = f'<b>Q.{q_odd_num} ({sub_lbl})</b>' if idx == 0 else f'({sub_lbl})'
            mod_disp = f'<b>MODULE {mod_num}</b>' if idx == 0 else ''
            marks_val = p.get('marks', 6)
            lvl_val = p.get('level', 'L2')
            co_val = p.get('co', co_tag)
            
            table_rows.append([
                Paragraph(mod_disp, ParagraphStyle('MC', parent=q_cell_style, alignment=1)),
                Paragraph(q_num_disp, ParagraphStyle('QC', parent=q_cell_style, alignment=1)),
                Paragraph(p.get('text', ''), q_cell_style),
                Paragraph(f'<b>{marks_val}M</b>', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
                Paragraph(f'{lvl_val}', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
                Paragraph(f'{co_val}', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
            ])
            curr_row += 1
            
        # OR ROW
        table_rows.append([
            Paragraph('', q_cell_style),
            Paragraph('', q_cell_style),
            Paragraph('<b>— OR —</b>', or_style),
            Paragraph('', q_cell_style),
            Paragraph('', q_cell_style),
            Paragraph('', q_cell_style)
        ])
        tstyles.append(('BACKGROUND', (0, curr_row), (-1, curr_row), colors.HexColor('#f1f5f9')))
        curr_row += 1

        # Question Even
        q_even = m.get('question_even', {})
        q_even_num = q_even.get('q_num', (mod_num-1)*2 + 2)
        parts_even = q_even.get('parts', [])
        
        for idx, p in enumerate(parts_even):
            sub_lbl = p.get('sub_q', 'a')
            q_num_disp = f'<b>Q.{q_even_num} ({sub_lbl})</b>' if idx == 0 else f'({sub_lbl})'
            marks_val = p.get('marks', 6)
            lvl_val = p.get('level', 'L2')
            co_val = p.get('co', co_tag)
            
            table_rows.append([
                Paragraph('', q_cell_style),
                Paragraph(q_num_disp, ParagraphStyle('QC', parent=q_cell_style, alignment=1)),
                Paragraph(p.get('text', ''), q_cell_style),
                Paragraph(f'<b>{marks_val}M</b>', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
                Paragraph(f'{lvl_val}', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
                Paragraph(f'{co_val}', ParagraphStyle('C', parent=q_cell_style, alignment=1)),
            ])
            curr_row += 1

    q_table = Table(table_rows, colWidths=[65, 55, 270, 45, 40, 45])
    q_table.setStyle(TableStyle(tstyles))
    story.append(q_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph('<div align="center"><b>*** END OF QUESTION PAPER ***</b></div>', note_style))

    doc.build(story)
    return buffer.getvalue()
