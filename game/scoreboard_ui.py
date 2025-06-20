from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QTabWidget, QLabel
import sys

class ScoreboardViewer(QWidget):
    def __init__(self, highest_scores, total_scores, player_scores):
        super().__init__()
        self.setWindowTitle("Scoreboard Rankings")
        self.resize(700, 400)

        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.create_table(highest_scores, 'Highest Score'), "Top Scores")
        tabs.addTab(self.create_table(total_scores, 'Total Score'), "All Time")
        tabs.addTab(self.create_table(player_scores, 'Score', personal=True), "My Scores")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def create_table(self, data, score_key, personal=False):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(3 if personal else 4)

        headers = ['Rank', 'Name', score_key] if personal else ['Rank', 'Name', 'Address', score_key]
        table.setHorizontalHeaderLabels(headers)

        for i, entry in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(entry['name']))
            if personal:
                table.setItem(i, 2, QTableWidgetItem(str(entry[score_key.lower().replace(' ', '_')])))
            else:
                table.setItem(i, 2, QTableWidgetItem(entry['player'][:10] + "..."))
                table.setItem(i, 3, QTableWidgetItem(str(entry[score_key.lower().replace(' ', '_')])))

        table.resizeColumnsToContents()

        return table

    def create_player_tab(self, player):
        table = QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Highest Score", "Total Score"])

        table.setItem(0, 0, QTableWidgetItem(player["name"]))
        table.setItem(0, 1, QTableWidgetItem(str(player["highest_score"])))
        table.setItem(0, 2, QTableWidgetItem(str(player["total_score"])))

        table.resizeColumnsToContents()

        return table


def view_scoreboard(highest_scores, total_scores, player_data):
    app = QApplication(sys.argv)
    window = ScoreboardViewer(highest_scores, total_scores, player_data)
    window.show()
    sys.exit(app.exec_())
