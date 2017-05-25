#!/usr/bin/env python
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer
import sys
import hkeys
import ahkeys
import etradepy

class EtradeApp(QtGui.QMainWindow, ahkeys.Ui_MainWindow):
    def __init__(self, parent=None):
        super(EtradeApp, self).__init__(parent)
        self.setupUi(self)

        self.cleartimer = QTimer()
        self.cleartimer.timeout.connect(lambda : self.statusBar.showMessage( "" ) )

        try:
            #
            self.Buy_1.clicked.connect(lambda : self.buy(self.T_1, self.qty_1))
            self.Buy_2.clicked.connect(lambda : self.buy(self.T_2, self.qty_2))
            self.Buy_3.clicked.connect(lambda : self.buy(self.T_3, self.qty_3))
            self.Buy_4.clicked.connect(lambda : self.buy(self.T_4, self.qty_4))
            self.Buy_5.clicked.connect(lambda : self.buy(self.T_5, self.qty_5))
            #
            self.Sell_1.clicked.connect(lambda : self.sell(self.T_1, self.qty_1))
            self.Sell_2.clicked.connect(lambda : self.sell(self.T_2, self.qty_2))
            self.Sell_3.clicked.connect(lambda : self.sell(self.T_3, self.qty_3))
            self.Sell_4.clicked.connect(lambda : self.sell(self.T_4, self.qty_4))
            self.Sell_5.clicked.connect(lambda : self.sell(self.T_5, self.qty_5))
            #
            self.SLimit_1.clicked.connect(lambda : self.slimit(self.T_1, self.qty_1, self.price_1))
            self.SLimit_2.clicked.connect(lambda : self.slimit(self.T_2, self.qty_2, self.price_2))
            self.SLimit_3.clicked.connect(lambda : self.slimit(self.T_3, self.qty_3, self.price_3))
            self.SLimit_4.clicked.connect(lambda : self.slimit(self.T_4, self.qty_4, self.price_4))
            self.SLimit_5.clicked.connect(lambda : self.slimit(self.T_5, self.qty_5, self.price_5))
            #
            self.SLoss_1.clicked.connect(lambda : self.stoploss(self.T_1, self.qty_1, self.loss_1))
            self.SLoss_2.clicked.connect(lambda : self.stoploss(self.T_2, self.qty_2, self.loss_2))
            self.SLoss_3.clicked.connect(lambda : self.stoploss(self.T_3, self.qty_3, self.loss_3))
            self.SLoss_4.clicked.connect(lambda : self.stoploss(self.T_4, self.qty_4, self.loss_4))
            self.SLoss_5.clicked.connect(lambda : self.stoploss(self.T_5, self.qty_5, self.loss_5))
            #
            self.T_1.textChanged.connect(lambda : self.ticker_1.setText(self.T_1.toPlainText()))
            self.T_2.textChanged.connect(lambda : self.ticker_2.setText(self.T_2.toPlainText()))
            self.T_3.textChanged.connect(lambda : self.ticker_3.setText(self.T_3.toPlainText()))
            self.T_4.textChanged.connect(lambda : self.ticker_4.setText(self.T_4.toPlainText()))
            self.T_5.textChanged.connect(lambda : self.ticker_5.setText(self.T_5.toPlainText()))
        except AttributeError:
            self.qty_1.setPlainText( '0' )
            self.qty_2.setPlainText( '0' )
            self.qty_3.setPlainText( '0' )
            #
            self.B1K_1.clicked.connect(lambda : self.accumulate(self.T_1, 1000, self.qty_1))
            self.B1K_2.clicked.connect(lambda : self.accumulate(self.T_2, 1000, self.qty_2))
            self.B1K_3.clicked.connect(lambda : self.accumulate(self.T_3, 1000, self.qty_3))
            #
            self.B2K_1.clicked.connect(lambda : self.accumulate(self.T_1, 2000, self.qty_1))
            self.B2K_2.clicked.connect(lambda : self.accumulate(self.T_2, 2000, self.qty_2))
            self.B2K_3.clicked.connect(lambda : self.accumulate(self.T_3, 2000, self.qty_3))
            #
            self.SAll_1.clicked.connect(lambda : self.accumulate(self.T_1, -int(self.qty_1.toPlainText()), self.qty_1 ))
            self.SAll_2.clicked.connect(lambda : self.accumulate(self.T_2, -int(self.qty_2.toPlainText()), self.qty_2 ))
            self.SAll_3.clicked.connect(lambda : self.accumulate(self.T_3, -int(self.qty_3.toPlainText()), self.qty_3 ))
            #
            self.SHalf_1.clicked.connect(lambda : self.accumulate(self.T_1, -int(self.qty_1.toPlainText())/2, self.qty_1 ))
            self.SHalf_2.clicked.connect(lambda : self.accumulate(self.T_2, -int(self.qty_2.toPlainText())/2, self.qty_2 ))
            self.SHalf_3.clicked.connect(lambda : self.accumulate(self.T_3, -int(self.qty_3.toPlainText())/2, self.qty_3 ))
            #
            self.T_1.textChanged.connect(lambda : self.ticker_1.setText(self.T_1.toPlainText()))
            self.T_2.textChanged.connect(lambda : self.ticker_2.setText(self.T_2.toPlainText()))
            self.T_3.textChanged.connect(lambda : self.ticker_3.setText(self.T_3.toPlainText()))
        self.Arm.stateChanged.connect(self.arm)

    def accumulate(self, ticker, qty, counter):
        if qty < 0:
            result = self.sell(ticker, -qty)
        else:
            result = self.buy(ticker, qty)
        if result:
            print counter.toPlainText()
            print qty
            counter.setPlainText(str(int(counter.toPlainText()) + int(qty)))


    def buy(self, ticker, qty):
        self.statusBar.showMessage( "Pending..." )
        try:
            qty = qty.toPlainText()
        except AttributeError:
            pass
        return self.report( etradepy.buyNow( trading_account, ticker.toPlainText(), qty ) )

    def sell(self, ticker, qty):
        try:
            qty = qty.toPlainText()
        except AttributeError:
            pass
        self.status_msg( "Pending..." )
        return self.report( etradepy.sellNow( trading_account, ticker.toPlainText(), qty ) )

    def slimit(self, ticker, qty, price):
        self.status_msg( "Pending..." )
        return self.report( etradepy.sellLimitNow( trading_account, ticker.toPlainText(), qty.toPlainText(),price.toPlainText() ) )

    def stoploss(self, ticker, qty, trailing):
        self.status_msg( "Pending..." )
        return self.report( etradepy.sellStopNow( trading_account, ticker.toPlainText(), qty.toPlainText(),trailing.toPlainText() ) )

    def report(self, response):
        print response
        if 'Error' in response:
            self.status_msg( response['Error']['message'] )
            return False
        else:
            self.status_msg( response['PlaceEquityOrderResponse']['EquityOrderResponse']['messageList']['msgDesc'] )
            return True

    def status_msg( self, message ):
        self.statusBar.showMessage( message )
        self.cleartimer.start(9000)

    def arm(self, int):
        state = self.Arm.isChecked()
        w = self.centralwidget
        p = w.palette()
        if state:
            p.setColor(w.backgroundRole(),QtGui.QColor(255,148,60))
        else:
            p.setColor(w.backgroundRole(),QtGui.QColor(73, 143, 255))
        w.setPalette(p)

        try:
            #
            self.Buy_1.setEnabled(state)
            self.Sell_1.setEnabled(state)
            self.SLimit_1.setEnabled(state)
            self.SLoss_1.setEnabled(state)
            #
            self.Buy_2.setEnabled(state)
            self.Sell_2.setEnabled(state)
            self.SLimit_2.setEnabled(state)
            self.SLoss_2.setEnabled(state)
            #
            self.Buy_3.setEnabled(state)
            self.Sell_3.setEnabled(state)
            self.SLimit_3.setEnabled(state)
            self.SLoss_3.setEnabled(state)
            #
            self.Buy_4.setEnabled(state)
            self.Sell_4.setEnabled(state)
            self.SLimit_4.setEnabled(state)
            self.SLoss_4.setEnabled(state)
            #
            self.Buy_5.setEnabled(state)
            self.Sell_5.setEnabled(state)
            self.SLimit_5.setEnabled(state)
            self.SLoss_5.setEnabled(state)
        except AttributeError:
            #
            self.B1K_1.setEnabled(state)
            self.B2K_1.setEnabled(state)
            self.SAll_1.setEnabled(state)
            self.SHalf_1.setEnabled(state)
            #
            self.B1K_2.setEnabled(state)
            self.B2K_2.setEnabled(state)
            self.SAll_2.setEnabled(state)
            self.SHalf_2.setEnabled(state)
            #
            self.B1K_3.setEnabled(state)
            self.B2K_3.setEnabled(state)
            self.SAll_3.setEnabled(state)
            self.SHalf_3.setEnabled(state)


def main():
    global trading_account

    # start connection to etrade
    etradepy.login()
    accounts =  etradepy.listAccounts()
    trading_account = accounts['json.accountListResponse']['response'][0]['accountId']

    app = QtGui.QApplication(sys.argv)
    form = EtradeApp()
    form.show()
    form.statusBar.showMessage( accounts['json.accountListResponse']['response'][0]['accountDesc'])
    app.exec_()

if __name__ == '__main__':
    main()

