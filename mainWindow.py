import datetime # ----------------------------------------------------------①
from PyQt5 import QtWidgets
from PyQt5 import QtGui # ---------------------------------------------------①
import Yuzuki_YukariUI
import yukari

class MainWindow(QtWidgets.QMainWindow):    
    """MainWindowクラス
    
    QtWidgets.QMainWindowを継承したサブクラス
    UI画面の構築を行う
    
    Attributes:
      action (bool): ラジオボタンの状態を保持する。
      yukari (obj:`yukari`): yukariオブジェクトを保持する。
      ui (obj:`Ui_MainWindow`): Ui_MainWindowオブジェクトを保持する。      
      
    """
        
    def __init__(self):
        """初期化のための処理を行う
        
        ・スーパークラスの__init__()を呼び出す。
        ・yukariオブジェクトを生成してself.yukariに格納。
        ・ラジオボタンの状態を保持する変数をTrueに初期化。
        ・setupUi（）を実行してUI画面を構築する。
        
        """
        super().__init__()
        self.yukari = yukari.yukari('yukari') # yukariオブジェクトを生成。
        self.action = True                    # ラジオボタンの状態を初期化。
        self.ui = Yuzuki_YukariUI.Ui_MainWindow() # Ui_MainWindowオブジェクトを生成。
        self.log = []                         # ログ用のリストを用意。------------②
        # setupUi()で画面を構築。MainWindow自身を引数にすることが必要。
        self.ui.setupUi(self)
        
    def putlog(self, str):
        """ 対話ログをリストに追加するメソッド。
        
        Parameters:
          str(str): ユーザーの入力または応答メッセージをログ用に整形した文字列。       
        """
        # QListWidgetクラスのaddItem()でログをリストに追加する。
        self.ui.listWidgetLog.addItem(str)
        # ユーザーからのメッセージ、ピティナの応答に改行を付けてlogに追加
        self.log.append(str + '\n') # --------------------------------------③
    def prompt(self):
        """ ピティナのプロンプトを作るメソッド。
        
        Returns:
          str: プロンプトを作る文字列。
        """
        # yukariクラスのget_name()でオブジェクト名を取得
        p = self.yukari.get_name()
        # 「Responderを表示」がオンならオブジェクト名を付加する
        if self.action == True:
            p += '：' + self.yukari.get_responder_name()
            
        # プロンプト記号を付けて返す
        return p + '> '

    def change_looks(self): # -----------------------------------------------②
        """機嫌値によってピティナの表情を切り替えるメソッド
        
        """
        # 応答フレーズを返す直前のピティナの機嫌値を取得
        em = self.yukari.emotion.mood
        # デフォルトの表情
        if -2 <= em < 1.5:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/img/talk.gif"))
        # ちょっと不機嫌な表情
        elif -5 <= em < -2:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/img/empty.gif"))
        # 怒った表情
        elif -10 <= em < -5:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/img/angry.gif"))
        # 嬉しさ爆発の表情
        elif 1.5 <= em <= 15:
            self.ui.labelShowImg.setPixmap(QtGui.QPixmap(":/re/img/happy.gif"))

      
    def writeLog(self): # --------------------------------------------------④
        """ ログを更新日時と共にログファイルに書き込む
        
        """
        # ログタイトルと更新日時のテキストを作成 
        # 日時は2020-01-01 00:00::00の書式にする
        now = 'Yukari System Dialogue Log: '\
              + datetime.datetime.now().strftime('%Y-%m-%d %H:%m::%S')\
              + '\n'
                      
        # リストlogの先頭要素として更新日時を追加
        self.log.insert(0, now)
        # logのすべての要素をログファイルへに書き込む
        with open('dics/log.txt', 'a', encoding = 'utf_8') as f:
            f.writelines(self.log)        

    def buttonTalkSlot(self):
        """ [話す]ボタンのイベントハンドラー
        
        ・yukariクラスのdialogue()を実行して応答メッセージを取得
        ・入力文字列および応答メッセージをログに出力
        
        """
        # ラインエディットのテキストを取得
        value = self.ui.lineEdit.text()
        
        if not value:
            # 入力エリアが未入力の場合は「なに?」と表示。
            self.ui.labelResponce.setText('なに?')
        else:
            # 入力されていたら対話オブジェクトを実行
            # インプット文字列を引数にしてdialogue()を実行し、応答メッセージを取得
            response = self.yukari.dialogue(value)
            # ピティナの応答メッセージをラベルに出力
            self.ui.labelResponce.setText(response)
            # プロンプト記号にインプット文字列を連結してログ用のリストに出力
            self.putlog('> ' + value)
            # ピティナ専用のプロンプト記号に応答メッセージを連結してログ用のリストに出力
            self.putlog(self.prompt() + response)
            # QLineEditクラスのclear()メソッドでラインエディットのテキストをクリア
            self.ui.lineEdit.clear()
            
        # ピティナのイメージを現在の機嫌値に合わせる
        self.change_looks() # -----------------------------------------------③
            
    def closeEvent(self, event): # -----------------------------------------⑤
        """ウィジェットの閉じるイベントでコールされるイベントハンドラー。
        
        ウィジェットを閉じるclose()メソッド実行時にQCloseEventによって呼ばれる。
        
        Overrides:
          ・メッセージボックスを表示する。
          ・[Yes]がクリックされたらイベントを続行してウィジェットを閉じる。
          ・[No]がクリックされたらイベントを取り消してウィジェットを閉じないようにする。          
          
        Parameters:
          event(QCloseEvent): 閉じるイベント発生時に渡されるQCloseEventオブジェクト。       

        """
        # メッセージボックスを表示
        reply = QtWidgets.QMessageBox.question(
                self,
                'あのねー',                 # タイトル
                "辞書を更新してもいい?", # メッセージ
                # Yes|Noボタンを表示する。
                buttons = QtWidgets.QMessageBox.Yes |
                          QtWidgets.QMessageBox.No
                )
        
        # [Yes]クリックでウィジェットを閉じ、[No]クリックで閉じる処理を無効にする。
        if reply == QtWidgets.QMessageBox.Yes:
            self.yukari.save()   # 記憶メソッド実行
            self.writeLog(     ) # 対話の一部始終をログファイルに保存
            event.accept()       # イベントを続行しcloseする。
        else:           
            event.accept()       # 即座にイベントを続行しcloseする。
    def showResponderName(self):
        """radioButton_1がオンになったときに呼ばれるイベントハンドラー
        
        ラジオボタンの状態を保持するactionの値をTrueにする
        
        """
        self.action = True
            
    def hiddenResponderName(self):
        """radioButton_2がオンになったときに呼ばれるイベントハンドラー
        
        ラジオボタンの状態を保持するactionの値をFalseにする
        
        """
        self.action = False

