import re
import random

class PatternItem:
    """パターン辞書1行の情報を保持するクラス
    
    Attributes: すべて「パターン辞書1行」あたりのデータ。
      modify (int): 機嫌変動値。
      pattern (str): 正規表現パターン。
      phrases(dicのlist):
          リスト要素の辞書は"応答フレーズ1個"の情報を持つ。
          {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
          これを1行の応答フレーズグループの数だけ持つ。
    """
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """PatternItemの初期化メソッド
        
        Parameters:
            pattern(str): パターン辞書1行の正規表現パターン。
            phrases(str）: パターン辞書1行の応答フレーズグループ。

        """        
        # self.modify、self.patternの初期化。
        self.initModifyAndPattern(pattern)
        # self.phrasesの初期化。
        self.initPhrases(phrases)

    def initModifyAndPattern(self, pattern):
        """self.modify(int)、self.pattern(str)の初期化を行う。
        
        パターン辞書の正規表現パターンの部分にSEPARATORをパターンマッチさせる。
        マッチ結果のリストから機嫌変動値と正規表現パターンを取り出し、
        self.modifyとself.patternに代入する。
        
        Parameters:
            pattern(str): パターン辞書1行の正規表現パターン。
        
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる。
        m = re.findall(PatternItem.SEPARATOR, pattern)
        # 機嫌変動値を保持するインスタンス変数を0で初期化。
        self.modify = 0
        # マッチ結果からパターン部分を取り出して
        # マッチ結果の整数の部分が空でなければ機嫌変動値をself.modifyに代入。
        if m[0][1]:
          self.modify =int(m[0][1])
        # マッチ結果からパターン部分を取り出してself.patternに代入。
        self.pattern = m[0][2]
        
    def initPhrases(self, phrases):
        """self.phrases(dicのlist)の初期化を行う。
        
        パターン辞書の応答フレーズグループにSEPARATORをパターンマッチさせる。
        マッチ結果のリストから"応答フレーズ1個"の必要機嫌値と応答フレーズを取り出して
          {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
        の辞書を作成。これを応答フレーズグループの数だけ繰り返す。
        
        作成した辞書はリストself.phrasesの要素にする。
        
        Parameters:
            phrases(str）: パターン辞書1行の応答フレーズグループ。
        """
        # リスト型のインスタンス変数を用意
        self.phrases = []
        # dic型のローカル変数
        dic = {}
        # 引数で渡された応答フレーズグループを'|'で分割し、
        # 1個の応答フレーズに対してSEPARATORをパターンマッチさせる。
        # {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}を作成し、
        # リストself.phrasesに格納する。
        for phrase in phrases.split('|'):
            # 1個の応答フレーズに対してパターンマッチを行う
            m = re.findall(PatternItem.SEPARATOR, phrase)
            # 'need'キーの値を必要機嫌値m[0][1]にする
            # 'phrase'キーの値を応答フレーズm[0][2]にする
            dic['need'] = 0
            if m[0][1]:
                dic['need'] = int(m[0][1])
            dic['phrase'] = m[0][2]
            # 作成した辞書をリストphrasesに追加
            self.phrases.append(dic.copy())

    def match(self, str):
        """ユーザーのメッセージにself.pattern(パターン辞書1行の正規表現パターン)
           がマッチするかを調べる
           
        Parameters:
            str(str): ユーザーが入力したメッセージ。
            
        Returns:
            Matchオブジェクト、マッチしない場合はNoneを返す。

        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        """現在の機嫌値と必要機嫌値を比較し、適切な応答フレーズを返す
        
        Parameters:
            mood(int）: ピティナの現在の機嫌値。        

        Returns:
            str:
                必要機嫌値をクリアした応答フレーズのリストからランダムチョイスした応答。
            None:
                クリアする応答フレーズがない場合はNone。
                     
        """
        choices = []
        # self.phrasesが保持する'need''phrase'の辞書を反復処理する
        for p in self.phrases:
            # self.phrasesの'need'キーの数値とパラメーターmoodをsuitable()に渡す
            # 必要機嫌値による条件をクリア（戻り値がTrue）であれば、
            # 対になっている応答フレーズをchoicesリストに追加する
            if (self.suitable(p['need'], mood)):
                choices.append(p['phrase'])
        # choicesリストが空であればNoneを返す
        if (len(choices) == 0):
            return None
        # choicesリストからランダムに応答フレーズを抽出して返す
        return random.choice(choices)

    def suitable(self, need, mood):
        """現在の機嫌値が必要機嫌値の条件を満たすかを判定
            
        Parameters:
            need(int): 必要機嫌値
            mood(int): 現在の機嫌値      

        Returns:
            bool:必要機嫌値をクリアしていたらTrue、そうでなければFalse。

        """
        # 必要機嫌値が0であればTrueを返す
        if (need == 0):
            return True
        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (need > 0):
            return (mood > need)
        # 応答例の数値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < need)

    def add_phrase(self, phrase): # ------------------------------------①
        """ユーザーメッセージの形態素が既存のパターン文字列とマッチした場合に、
           Dictionaryのstudy_pattern()メソッドから呼ばれる。
        
        パターン辞書1行の応答フレーズグループ末尾に、ユーザーメッセージを
        新規の応答フレーズとして追加する。
           
        Parameters:
            phrase(str): ユーザーのメッセージ
            
        """
        # 既存の応答フレーズにユーザーのメッセージが一致するかを順次調べ、
        # 一致するフレーズがあった時点でreturnしてメソッドを終了。
        #
        # self.phrases(dicのlist):
        #　　　　リスト要素の辞書は"応答フレーズ1個"の情報を持つ。
        #     [{'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}, ...]
        # 
        # Block Parameters:
        #     p(dic): 必要機嫌値と応答フレーズ1個の情報を持つ。
        for p in self.phrases: # ---------------------------------------②
            if p['phrase'] == phrase:
                return
        # リストself.phrasesに、{'need':0, 'phrase':'ユーザーのメッセージ'}を追加。
        self.phrases.append({'need': 0, 'phrase': phrase}) # -----------③
        
    def make_line(self): # ---------------------------------------------④
        """パターン辞書1行ぶんのデータを作る
        
        Returns:
            str: パターン辞書用に成形したデータ。
        """
        # '機嫌変動値##パターン文字列'を作る
        pattern = str(self.modify) + '##' + self.pattern # -------------⑤
        # 応答フレーズグループ用のリスト
        pr_list = [] # -------------------------------------------------⑥
        
        # 応答フレーズのグループを作成する。
        #
        # Block Parameters:
        #    p(dic): 必要機嫌値と応答フレーズ1個の情報を持つ。
        for p in self.phrases:
            # '必要機嫌値##応答フレーズ'を作ってリストに追加する。
            pr_list.append(str(p['need']) + '##' + p['phrase'])
        
        # '機嫌変動値##パターン文字列[TAB]' に|で区切った
        # '必要機嫌値##応答フレーズ' のグループを連結して返す
        return pattern + '\t' + '|'.join(pr_list)

