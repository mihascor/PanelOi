from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from app.services.build_oi_price_chart import build_oi_price_chart_data
import pyqtgraph as pg
import numpy as np

class AnalysisWindow(QDialog):
    def __init__(self, paper: str):
        super().__init__()

        self.setWindowTitle(f"Анализ: {paper}")
        data = build_oi_price_chart_data(paper)

        layout = QVBoxLayout()

        title_label = QLabel(paper)
        title_label.setObjectName("analysisTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- подготовка данных ---
        dates = list(range(len(data["dates"])))

        # --- графики ---
        price_plot = pg.PlotWidget()
        oi_plot = pg.PlotWidget()

        # --- синхронизация ---
        oi_plot.setXLink(price_plot)

        # --- цена (high/low вертикали) ---
        for i in range(len(dates)):
            x = dates[i]
            high = data["price_high"][i]
            low = data["price_low"][i]

            if high is None or low is None:
                continue

            price_plot.plot([x, x], [low, high], pen=pg.mkPen("w"))

        # --- OI ---
        fiz_pen = pg.mkPen("g", width=2)
        yur_pen = pg.mkPen("r", width=2)

        fiz = [v if v is not None else np.nan for v in data["fiz_koof"]]
        yur = [v if v is not None else np.nan for v in data["yur_koof"]]

        oi_plot.plot(dates, fiz, pen=fiz_pen)
        oi_plot.plot(dates, yur, pen=yur_pen)

        # --- ограничения ---
        oi_plot.setYRange(-20, 20)

        zero_line = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen("gray"))
        oi_plot.addItem(zero_line)

        # --- layout ---
        layout.addWidget(title_label)
        layout.addWidget(price_plot)
        layout.addWidget(oi_plot)

        self.setLayout(layout)
