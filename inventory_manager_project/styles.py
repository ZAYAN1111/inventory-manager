LIGHT_STYLE = """
QWidget{background:#f0f2f5;color:#1a1a1a;font-size:11pt;font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;}

QFrame#Card{background:white;border:1px solid #e2e5e9;border-radius:12px;}
QFrame#Card:hover{border:1px solid #3498db;}

QPushButton{background:#3498db;color:white;border:none;padding:9px 16px;border-radius:8px;font-weight:600;}
QPushButton:hover{background:#2f8bcb;}
QPushButton:pressed{background:#2678b0;}
QPushButton:disabled{background:#b8c4cc;color:#eef1f4;}
QPushButton#DeleteBtn{background:#e74c3c;}
QPushButton#DeleteBtn:hover{background:#d63e2e;}
QPushButton#DeleteBtn:pressed{background:#c0392b;}

QLineEdit,QSpinBox,QComboBox,QDateEdit{
    background:white;color:#1a1a1a;border:1px solid #d7dce1;
    border-radius:8px;padding:7px 10px;selection-background-color:#3498db;
}
QLineEdit:focus,QSpinBox:focus,QComboBox:focus,QDateEdit:focus{border:1px solid #3498db;}
QLineEdit:hover,QSpinBox:hover,QComboBox:hover,QDateEdit:hover{border:1px solid #b3bcc4;}
QComboBox::drop-down{border:none;width:24px;}

QTableWidget,QListWidget{
    background:white;color:#1a1a1a;border:1px solid #e2e5e9;border-radius:8px;
    gridline-color:#eef1f4;alternate-background-color:#f7f9fb;
}
QHeaderView::section{background:#f7f9fb;color:#4a4f57;border:none;border-bottom:2px solid #e2e5e9;padding:6px;font-weight:600;}
QTableWidget::item:selected,QListWidget::item:selected{background:#dceefb;color:#1a1a1a;}

QMenuBar{background:#f0f2f5;color:#1a1a1a;padding:4px;}
QMenuBar::item{padding:6px 12px;border-radius:6px;}
QMenuBar::item:selected{background:#e2e5e9;}
QMenu{background:white;color:#1a1a1a;border:1px solid #e2e5e9;border-radius:8px;}
QMenu::item{padding:6px 20px;}
QMenu::item:selected{background:#dceefb;border-radius:4px;}

QProgressBar{background:#eef1f4;border:none;border-radius:8px;text-align:center;color:#1a1a1a;font-weight:600;min-height:22px;}
QProgressBar::chunk{border-radius:8px;}

QSlider::groove:horizontal{background:#d7dce1;height:4px;border-radius:2px;}
QSlider::handle:horizontal{background:#3498db;width:16px;height:16px;margin:-6px 0;border-radius:8px;}
QSlider::handle:horizontal:hover{background:#2f8bcb;}

QScrollArea{background:#f0f2f5;border:none;}
QScrollBar:vertical{background:transparent;width:12px;margin:2px;}
QScrollBar::handle:vertical{background:#c7ccd1;border-radius:5px;min-height:30px;}
QScrollBar::handle:vertical:hover{background:#a9afb6;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}

QCheckBox{spacing:8px;}
QCheckBox::indicator{width:18px;height:18px;border-radius:4px;border:1px solid #d7dce1;background:white;}
QCheckBox::indicator:checked{background:#3498db;border:1px solid #3498db;}

QToolTip{background:#2c2c2c;color:white;border:none;padding:6px 10px;border-radius:6px;}

QLabel#EmptyState{color:#8a929b;font-size:13pt;}
"""

DARK_STYLE = """
QWidget{background:#181818;color:#e8e8e8;font-size:11pt;font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;}

QFrame#Card{background:#232323;border:1px solid #34363a;border-radius:12px;}
QFrame#Card:hover{border:1px solid #2d7dbf;}

QPushButton{background:#2d7dbf;color:white;border:none;padding:9px 16px;border-radius:8px;font-weight:600;}
QPushButton:hover{background:#3690db;}
QPushButton:pressed{background:#2670aa;}
QPushButton:disabled{background:#3a3d42;color:#75797f;}
QPushButton#DeleteBtn{background:#c0392b;}
QPushButton#DeleteBtn:hover{background:#e74c3c;}
QPushButton#DeleteBtn:pressed{background:#a5311f;}

QLineEdit,QSpinBox,QComboBox,QDateEdit{
    background:#232323;color:#e8e8e8;border:1px solid #34363a;
    border-radius:8px;padding:7px 10px;selection-background-color:#2d7dbf;
}
QLineEdit:focus,QSpinBox:focus,QComboBox:focus,QDateEdit:focus{border:1px solid #2d7dbf;}
QLineEdit:hover,QSpinBox:hover,QComboBox:hover,QDateEdit:hover{border:1px solid #4a4d52;}
QComboBox::drop-down{border:none;width:24px;}

QTableWidget,QListWidget{
    background:#232323;color:#e8e8e8;border:1px solid #34363a;border-radius:8px;
    gridline-color:#34363a;alternate-background-color:#282828;
}
QHeaderView::section{background:#2a2a2a;color:#e8e8e8;border:none;border-bottom:2px solid #34363a;padding:6px;font-weight:600;}
QTableWidget::item:selected,QListWidget::item:selected{background:#254a63;color:#e8e8e8;}

QScrollArea{background:#181818;border:none;}
QScrollBar:vertical{background:transparent;width:12px;margin:2px;}
QScrollBar::handle:vertical{background:#3d3f43;border-radius:5px;min-height:30px;}
QScrollBar::handle:vertical:hover{background:#54575c;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}

QMenuBar{background:#181818;color:#e8e8e8;padding:4px;}
QMenuBar::item{padding:6px 12px;border-radius:6px;}
QMenuBar::item:selected{background:#2d7dbf;}
QMenu{background:#232323;color:#e8e8e8;border:1px solid #34363a;border-radius:8px;}
QMenu::item{padding:6px 20px;}
QMenu::item:selected{background:#2d7dbf;border-radius:4px;}

QProgressBar{background:#2a2a2a;border:none;border-radius:8px;color:#e8e8e8;text-align:center;font-weight:600;min-height:22px;}
QProgressBar::chunk{border-radius:8px;}

QSlider::groove:horizontal{background:#34363a;height:4px;border-radius:2px;}
QSlider::handle:horizontal{background:#2d7dbf;width:16px;height:16px;margin:-6px 0;border-radius:8px;}
QSlider::handle:horizontal:hover{background:#3690db;}

QCheckBox{spacing:8px;}
QCheckBox::indicator{width:18px;height:18px;border-radius:4px;border:1px solid #4a4d52;background:#232323;}
QCheckBox::indicator:checked{background:#2d7dbf;border:1px solid #2d7dbf;}

QToolTip{background:#0f0f0f;color:#e8e8e8;border:1px solid #34363a;padding:6px 10px;border-radius:6px;}

QLabel#EmptyState{color:#75797f;font-size:13pt;}
"""

# Backwards-compatible default (light mode)
STYLE = LIGHT_STYLE


def get_style(dark_mode: bool) -> str:
    return DARK_STYLE if dark_mode else LIGHT_STYLE
