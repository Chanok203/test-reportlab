#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
import pytz
import re
tz = pytz.timezone('Asia/Bangkok')

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (Frame, Paragraph, BaseDocTemplate, PageTemplate, FrameBreak, PageBreak, NextPageTemplate, TableStyle, Flowable, Image)
from reportlab.platypus.tables import Table
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER


registerFont(TTFont('THSarabun', './font/THSarabunNew.ttf'))
registerFont(TTFont('THSarabun-Bd', './font/THSarabunNew Bold.ttf'))
registerFont(TTFont('THSarabun-It', './font/THSarabunNew Italic.ttf'))
registerFont(TTFont('THSarabun-BdIt', './font/THSarabunNew BoldItalic.ttf'))


def secure_filename(string):
    pattern = re.compile(r"[^\u0E00-\u0E7Fa-zA-Z0-9' ]|^'|'$|''")
    char_to_remove = re.findall(pattern, string)
    list_with_char_removed = [char for char in string if not char in char_to_remove]
    return ''.join(list_with_char_removed)

# In[3]:


def get_month_thai(month):
    return 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[month]


# In[4]:


class InteractiveCheckBox(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.rect(0, 0, self.width, self.height, fill=0)


# In[5]:


def addHead(story, data):
    story.append(
    Paragraph(
        'JEDMOVE Delivery',
        ParagraphStyle(
            name="left_frame1",
            alignment = TA_LEFT,
            fontName='THSarabun-Bd',
            fontSize=32,
        )))
    story.append(FrameBreak())

    # right_frame
    story.append(
        Paragraph(
            'ใบเสร็จรับเงิน',
            ParagraphStyle(
                name="right_frame1",
                alignment = TA_RIGHT,
                textColor = Color(red=0.7, green=0.7, blue=0.7, alpha=1),
                fontName='THSarabun-Bd',
                fontSize=32,
            )))
    story.append(FrameBreak())


    # company_frame
    story.append(
        Paragraph(
            'บริษัท เจดมูฟ เดลิเวอรี่ จำกัด',
            ParagraphStyle(
                name="company_frame1",
                alignment = TA_LEFT,
                textColor = Color(red=0.7, green=0.7, blue=0.7, alpha=1),
                fontName='THSarabun-BdIt',
                fontSize=18,
            )))
    story.append(FrameBreak())

    # company_detail_frame
    story.append(
        Paragraph(
            'เลขที่ 13/7 หมู่ 5 ถนนยิงเป้าใต้ ตำบลสนามจันทร์ อำเภอเมืองนครปฐม จังหวัดนครปฐม 73000 <br />โทร. 091-776-6570',
            ParagraphStyle(
                name="company_deatail_frame1",
                alignment = TA_LEFT,
                fontName='THSarabun',
                fontSize=18,
                leading=24,
            )))
    story.append(FrameBreak())

    # invoice_frame
    story.append(Table(
            [['วันที่:', data['today']],
            ['เลขที่ใบเสร็จ:', data['invoice_number']],
            ['สำหรับ:', 'ค่าบริการจัดส่งอาหาร']],
            style=TableStyle([
                ('FONTNAME', (0,0), (-2,-1), 'THSarabun-Bd'),
                ('FONTNAME', (1,0), (-1,-1), 'THSarabun'),
                ('FONTSIZE', (0,0), (-1,-1), 18),
                ('ALIGNMENT', (0,0), (-1,-1), 'RIGHT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('RIGHTPADDING',(0,0),(-1,-1),0),
                ('LEADING',(0,0),(-1,-1),20)
            ]),
            hAlign='RIGHT'
            ))
    story.append(FrameBreak())

    # shop_frame
    story.append(Table(
            [['เรียกเก็บไปยัง: ', 'ร้าน %s' % (data['shop_name'])]],
            style=TableStyle([
                ('FONTNAME', (0,0), (-2,-1), 'THSarabun-Bd'),
                ('FONTNAME', (1,0), (-1,-1), 'THSarabun'),
                ('FONTSIZE', (0,0), (-1,-1), 18),
                ('ALIGNMENT', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),0),
                ('LEADING',(0,0),(-1,-1),20)
            ]),
            hAlign='LEFT'
            ))
    story.append(FrameBreak())


# In[6]:


def addDetail(story, data, doc):
    story.append(Table(
        [["คำอธิบาย","รวม(บาท)","ค่าบริการ(บาท)"],
         ["ตั้งแต่ วันที่ %s\nถึง     วันที่ %s\nหมายเหตุ รายละเอียดอยู่หน้าถัดไป" % (data['start_date'], data['end_date']), 
          str(data['sum']), str(data['fee'])],
        ["ผลรวม", str(data['sum']), str(data['fee'])]],
        
        style=TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'THSarabun-Bd'),
            ('ALIGNMENT', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,0), 18),
            ('LEADING',(0,0),(-1,0),20),
            
            ('FONTNAME', (0,1), (-1,-1), 'THSarabun'),
            ('FONTSIZE', (0,1), (-1,-1), 16),
            ('LEADING',(0,1),(-1,-1), 24),
            
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID',(0,0),(-1,-1),0.5, Color(0,0,0)),
            
            ('ALIGNMENT', (0,1), (0,1), 'LEFT'),
            
            ('FONTNAME', (0,-1), (-1,-1), 'THSarabun-Bd'),
            ('ALIGNMENT', (0,-1), (0,-1), 'RIGHT'),
            ('FONTSIZE', (0,-1), (-1,-1), 20),
            ('LEADING',(0,-1),(-1,-1), 28),
        ]),
        hAlign='CENTER',
        vAlign='TOP',
        colWidths= list(map( lambda x: x*doc.width ,[ 0.6, 0.2, 0.2 ]))
        ))
    story.append(FrameBreak())


# In[7]:


def create_invoice(path, data):
    doc = BaseDocTemplate(
                path,
                title=data['title'],
                showBoundary=0,
                pagesize=portrait(A4),
                topMargin=0.6*inch,
                bottomMargin=0.75*inch,
                leftMargin=0.7*inch,
                rightMargin=0.7*inch)
    addTemplates(doc)
    story = []
    addHead(story, data)
    addDetail(story, data, doc)
    addFooter(story, data, doc)
    story.append( NextPageTemplate('Page2') )
    story.append(PageBreak())
    addPage2(story, data, doc)
    
    doc.build(story)


# In[8]:


def addPage2(story, data, doc):
    # PAGE 2
    story.append(Table(
            [[
                Paragraph("รายละเอียด: ",style=ParagraphStyle(
                                name="pay_frame2",
                                alignment = TA_LEFT,
                                fontName='THSarabun-Bd',
                                fontSize=16,
                                leading=20,
                                )),
                Paragraph("ร้าน %s<br />ตั้งแต่ วันที่ %s ถึง วันที่ %s" % (data['shop_name'], data['start_date'], data['end_date']),
                          style=ParagraphStyle(
                                name="pay_frame2",
                                alignment = TA_LEFT,
                                fontName='THSarabun',
                                fontSize=14,
                                leading=18,
                                )),
            ]],
            style=TableStyle([
                ('VALIGN', (0,0), (0,-1), 'TOP'),
                ('VALIGN', (1,0), (-1,-1), 'MIDDLE'),
                ('ALIGNMENT', (0,0), (-1, -1), 'LEFT'),
    #             ('GRID',(0,0),(-1,-1),0.5, Color(0,0,0)),
            ]),
            hAlign='LEFT',
            vAlign='TOP',
            colWidths= list(map( lambda x: x*doc.width ,[ 0.14, 0.86]))
        ))

    story.append(Table(
            [
                ["คำอธิบาย","รวม(บาท)","ค่าบริการ(บาท)"],
            ] + data['detail'] + [
                ["ผลรวม", str(data['sum']), str(data['fee'])]
            ],
            style=TableStyle([
                ('FONTNAME', (0,0), (-1,0), 'THSarabun-Bd'),
                ('ALIGNMENT', (0,0), (-1,-1), 'CENTER'),
                ('FONTSIZE', (0,0), (-1,0), 16),
                ('LEADING',(0,0),(-1,0),18),

                ('FONTNAME', (0,1), (-1,-1), 'THSarabun'),
                ('FONTSIZE', (0,1), (-1,-1), 14),
                ('LEADING',(0,1),(-1,-1),15),

                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID',(0,0),(-1,-1),0.5, Color(0,0,0)),

                ('ALIGNMENT', (0,1), (0,-1), 'LEFT'),
                ('FONTNAME', (0,-1), (-1,-1), 'THSarabun-Bd'),
                ('FONTSIZE', (0,-1), (-1,-1), 18),
                ('LEADING',(0,-1),(-1,-1),20),
                ('ALIGNMENT', (0,-1), (0,-1), 'RIGHT'),

            ]),
            hAlign='CENTER',
            vAlign='TOP',
            colWidths= list(map( lambda x: x*doc.width ,[ 0.6, 0.2, 0.2]))
            ))

    
# In[9]:


def addTemplates(doc):
    left_frame_1 = Frame(
                x1=doc.leftMargin,
                y1=doc.height + doc.bottomMargin - doc.height/20,
                width=doc.width/2,
                height=doc.height/20,
                topPadding=0,
                bottomPadding=0,
                rightPadding=0,
                leftPadding=0)

    right_frame_1 = Frame(
                    x1=doc.leftMargin + doc.width/2,
                    y1=doc.height + doc.bottomMargin - doc.height/20,
                    width=doc.width/2,
                    height=doc.height/20,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)

    company_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*2,
                    width=doc.width,
                    height=doc.height/20,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)

    company_detail_frame = Frame(
                            x1=doc.leftMargin,
                            y1=doc.height + doc.bottomMargin - doc.height/20*5,
                            width=doc.width/2,
                            height=doc.height/20*3,
                            rightPadding=0,
                            leftPadding=0)

    invoice_frame = Frame(
                        x1=doc.leftMargin + doc.width/2,
                        y1=doc.height + doc.bottomMargin - doc.height/20*5,
                        width=doc.width/2,
                        height=doc.height/20*3,
                        rightPadding=0,
                        leftPadding=0)

    shop_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*6,
                    width=doc.width,
                    height=doc.height/20,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)

    table_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*10,
                    width=doc.width,
                    height=doc.height/20*4,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)

    pay_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*17,
                    width=doc.width/2,
                    height=doc.height/20*7,
                    topPadding=0.1*inch,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)
    
    qrcode_frame = Frame(
                        x1=doc.leftMargin + doc.width/2,
                        y1=doc.height + doc.bottomMargin - doc.height/20*17,
                        width=doc.width/2,
                        height=doc.height/20*7,
                        topPadding=0.5*inch,
                        bottomPadding=0,
                        rightPadding=0,
                        leftPadding=0)

    confirm_1_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*19,
                    width=doc.width/3,
                    height=doc.height/20*2,
                    topPadding=0.2*inch,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)
    
    confirm_2_frame = Frame(
                    x1=doc.leftMargin + doc.width/3,
                    y1=doc.height + doc.bottomMargin - doc.height/20*19,
                    width=doc.width/3,
                    height=doc.height/20*2,
                    topPadding=0.2*inch,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0.05*inch)

    footer_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.height + doc.bottomMargin - doc.height/20*20,
                    width=doc.width,
                    height=doc.height/20*1,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)

    # Page 2
    detail_frame = Frame(
                    x1=doc.leftMargin,
                    y1=doc.bottomMargin,
                    width=doc.width,
                    height=doc.height,
                    topPadding=0,
                    bottomPadding=0,
                    rightPadding=0,
                    leftPadding=0)


    doc.addPageTemplates( [
        PageTemplate(id='Page1', frames=[
            left_frame_1, right_frame_1, company_frame, company_detail_frame, invoice_frame, shop_frame, table_frame, 
            pay_frame, 
#             qrcode_frame,
            confirm_1_frame, confirm_2_frame ,
            footer_frame]),
        PageTemplate(id='Page2', frames=[detail_frame]),

    ])


# In[10]:


def addFooter(story, data, doc):
    # pay_frame
    story.append(
        Paragraph(
            'การชำระเงิน',
            ParagraphStyle(
                name="pay_frame1",
                alignment = TA_LEFT,
                fontName='THSarabun-Bd',
                fontSize=20,
                leading=30,
            )))
    story.append(Table(
            [[
                InteractiveCheckBox(10,10), Paragraph("เงินสด",style=ParagraphStyle(
                                name="pay_frame2",
                                alignment = TA_LEFT,
                                fontName='THSarabun',
                                fontSize=18,
                                leading=24,
                                )),
                InteractiveCheckBox(10,10), Paragraph("โอน",style=ParagraphStyle(
                                name="pay_frame2",
                                alignment = TA_LEFT,
                                fontName='THSarabun',
                                fontSize=18,
                                leading=24,
                                )),
            ]],
            style=TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGNMENT', (0,0), (0, 0), 'RIGHT'),
                ('ALIGNMENT', (1,0), (1, 0), 'LEFT'),
                ('ALIGNMENT', (2,0), (2, 0), 'RIGHT'),
                ('ALIGNMENT', (3,0), (3, 0), 'LEFT'),
    #             ('GRID',(0,0),(-1,-1),0.5, Color(0,0,0)),
            ]),
            hAlign='LEFT',
            vAlign='TOP',
            colWidths= list(map( lambda x: x*doc.width/2 ,[ 0.2, 0.2, 0.2, 0.2 ]))
            ))

    story.append(
        Paragraph(
            ' &nbsp;',
            ParagraphStyle(
                name="footer_frame1",
                alignment = TA_CENTER,
                fontName='THSarabun',
                fontSize=16,
                leading=16,
            ),
        ))
    
    # qrcode_frame
#     story.append(FrameBreak())
    story.append(
        Image('./qrcode_2.png', 
              width=(1079/1151)*inch*2.3,
              height=(1151/1151)*inch*2.3,
              hAlign='CENTER',
             )
    )
#     story.append(
#         Paragraph(
#             'สามารถสแกนคิวอาร์โค้ดเพื่อชำระเงิน',
#             ParagraphStyle(
#                 name="footer_frame1",
#                 alignment = TA_CENTER,
#                 fontName='THSarabun',
#                 fontSize=16,
#                 leading=26,
#             ),
#         ))

    story.append(FrameBreak())

    # confirm_1_frame
    story.append(
        Paragraph(
            'ลงชื่อ &nbsp;'+ '_' * 22 + ' &nbspผู้ชำระเงิน' + '<br />'*1 +
#             ' &nbsp;'*2 + '( ' + ' &nbsp;'*22 + ')'+ ' &nbsp;'*4 + '<br />'+
            ' วันที่ &nbsp' + '_'*22 + ' &nbsp;'*7,
            ParagraphStyle(
                name="confirm_frame1",
                alignment = TA_LEFT,
                fontName='THSarabun',
                fontSize=12,
                leading=18,
            )))
    story.append(FrameBreak())
    
     # confirm_2_frame
    story.append(
        Paragraph(
            'ลงชื่อ &nbsp;'+ '_' * 22 + ' &nbspผู้รับเงิน' + '<br />'*1 +
#             ' &nbsp;'*2 + '( ' + ' &nbsp;'*22 + ')'+ ' &nbsp;'*3 + '<br />'+
            ' วันที่  &nbsp' + '_'*22 + ' &nbsp;'*5,
            ParagraphStyle(
                name="confirm_frame1",
                alignment = TA_LEFT,
                fontName='THSarabun',
                fontSize=12,
                leading=18,
            )))
    story.append(FrameBreak())

    # footer_frame
    "นายวิศรุต ชอุ่มวรรณ"
    story.append(
        Paragraph(
            ' &nbsp<br />หากมีข้อสงสัยเกี่ยวกับใบเสร็จรับเงินนี้ สามารถติดต่อได้ที่ 091-776-6570',
            ParagraphStyle(
                name="footer_frame1",
                alignment = TA_LEFT,
                fontName='THSarabun',
                fontSize=14,
                leading=16,
            ),
        ))


# In[12]:


now = datetime.datetime.now(tz)
today = "%d %s %d" % (now.day, get_month_thai(now.month), now.year + 543)

data = {
    'title': 'Invoice',
    'today': today,
    'invoice_number': 12,
    'shop_name': 'หยก (เดโม)',
    'start_date': '%d %s %d' % (1, get_month_thai(2), 2020+543),
    'end_date': '%d %s %d' % (29, get_month_thai(2), 2020+543),
    'sum': int(2000),
    'fee': int(2000*0.15),
    'credit': int(5000-2000*0.15),
    'detail': [["วันที่   1 กุมภาพันธุ์ 2563 (10 รายการ)", "1000", "150", "4000"]] * 31,
}

path = 'test_invoice.pdf'

create_invoice(path, data)


# In[ ]:





# In[ ]:




