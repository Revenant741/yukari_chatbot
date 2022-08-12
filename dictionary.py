import random
import re

class Dictionary(object):
    """Dictionaryクラス
    
    ランダム辞書とパターン辞書を開き、データをインスタンス変数に格納する。

    Attributes:
      random (strのlist):
        ランダム辞書のすべてのフレーズを要素として格納。
        [フレーズ1, フレーズ2, フレーズ3, ...]
                     
      pattern (PatternItemのlist):
        [PatternItem1, PatternItem2, PatternItem3, ...]
                   
        PatternItem:
          "パターン辞書1行"の情報を持つ
          PatternItem.modify(int): 機嫌変動値。
          PatternItem.pattern(str): 正規表現パターン。
          PatternItem.phrases(dicのlist):
               リスト要素の辞書は"応答フレーズ1個"の情報を持つ。
               {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
               これを1行の応答フレーズグループの数だけ持つ。
      
    """
    def __init__(self):
        '''Dictionaryオブジェクトの初期化を行う。
        
        makeRandomList（）、makePatternDictionary()を実行して、
        ランダム応答用のリスト、パターン応答用の辞書オブジェクトを生成する。
        
        '''
        # ピティナのランダム辞書を作成。
        self.random = self.makeRandomList()
        # ピティナのパターン辞書を作成。
        self.pattern = self.makePatternDictionary()
        
    def makeRandomList(self):
        """ランダム辞書ファイルのデータを読み込んでリストrandomに格納する。
        
        Returns:
            strのlist: 要素はランダム辞書1行あたりの応答フレーズ。
        """
        # ランダム辞書ファイルオープン
        rfile = open('dics/random.txt', 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        r_lines = rfile.readlines()
        rfile.close()
        # 末尾の改行と空白文字を取り除いてリストに格納
        randomList = []
        for line in r_lines:
            str = line.rstrip('\n')
            if (str!=''):
                randomList.append(str)
        return randomList

    def makePatternDictionary(self):
        """パターン辞書ファイルのデータを読み込んでリストpatternに格納する。
        
        Returns:
            PatternItemのlist: PatternItemはパターン辞書1行の応答フレーズ1個の情報を持つ。
          
        """        
        # パターン辞書オープン
        pfile = open('dics/pattern.txt', 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        pfile.close()
        # 末尾の改行と空白文字を取り除いてリストに格納
        new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if (str!=''):
                new_lines.append(str)
             
        # パターン辞書の各行をタブで切り分けて以下の変数に格納。
        #
        # ptn パターン辞書1行の正規表現パターン。
        # prs パターン辞書1行の応答フレーズグループ。
        #
        # 引数をptn、prsにしてPatternItemオブジェクトを1個生成し、
        # patternItemList（リスト）に追加。パターン辞書の行の数だけ繰り返す。
        patternItemList = [] # ----------------------------------------①
        for line in new_lines:
            ptn, prs = line.split('\t')
            patternItemList.append(PatternItem(ptn, prs)) # -----------②
        return patternItemList
            
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
    SEPARATOR = '^((-?\d+)##)?(.*)$' # ------------------------①

    def __init__(self, pattern, phrases): # -------------------②
        """PatternItemの初期化メソッド
        
        Parameters:
            pattern(str): パターン辞書1行の正規表現パターン。
            phrases(dicのlist）: パターン辞書1行の応答フレーズグループ。

        """        
        # self.modify、self.patternの初期化。
        self.initModifyAndPattern(pattern)
        # self.phrasesの初期化。
        self.initPhrases(phrases)

    def initModifyAndPattern(self, pattern):
        """self.modify(int)、self.pattern(str)の初期化を行う。
        
        パターン辞書の正規表現パターンの部分にSEPARATORをパターンマッチさせる。、
        マッチ結果のリストから機嫌変動値と正規表現パターンを取り出し、
        self.modifyとself.patternに代入する。
        
        Parameters:
            pattern(str): パターン辞書1行の正規表現パターン。
        
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる。
        m = re.findall(PatternItem.SEPARATOR, pattern) # --------③
        # 機嫌変動値を保持するインスタンス変数を0で初期化。
        self.modify = 0 # -------------------------------------④
        # マッチ結果の整数の部分が空でなければ機嫌変動値をself.modifyに代入。
        if m[0][1]:
            self.modify = int(m[0][1]) # -------------------------⑤
        # マッチ結果からパターン部分を取り出してself.patternに代入。
        self.pattern = m[0][2] # ------------------------------⑥
        
    def initPhrases(self, phrases):
        """self.phrases(dicのlist)の初期化を行う。
        
        パターン辞書の応答フレーズグループにSEPARATORパターンマッチさせる。
        マッチ結果のリストから"応答フレーズ1個"の必要機嫌値と応答フレーズを取り出して
          {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
        の辞書を作成。これを応答フレーズグループの数だけ繰り返す。
        
        作成した辞書はリストself.phrasesの要素にする。
        
        Parameters:
            phrases(stｒ）: パターン辞書1行の応答フレーズグループ。
        """
        # リスト型のインスタンス変数を用意
        self.phrases = [] # -----------------------------------⑦
        # dic型のローカル変数
        dic = {}
        # 引数で渡された応答フレーズグループを'|'で分割し、
        # 1個の応答フレーズに対してSEPARATORをパターンマッチさせる。
        # {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}を作成し、
        # リストself.phrasesに格納する。
        for phrase in phrases.split('|'): # -------------------⑧
            # 1個の応答フレーズに対してパターンマッチを行う
            m = re.findall(PatternItem.SEPARATOR, phrase)
            # 'need'キーの値を必要機嫌値m[0][1]にする
            # 'phrase'キーの値を応答フレーズm[0][2]にする
            dic['need'] = 0
            if m[0][1]:
                dic['need'] = int(m[0][1])
            dic['phrase'] = m[0][2]
            # 作成した辞書をリストphrasesに追加
            self.phrases.append(dic.copy()) # -----------------⑨

    def match(self, str): # -----------------------------------⑩
        """ユーザーのメッセージにself.pattern(パターン辞書1行の正規表現パターン)
           がマッチするかを調べる
           
        Parameters:
            str(stｒ): ユーザーが入力したメッセージ。
            
        Returns:
            Matchオブジェクト、マッチしない場合はNoneを返す。

        """
        return re.search(self.pattern, str)

    def choice(self, mood): # ---------------------------------⑪
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
            if (self.suitable(p['need'], mood)): # ------------⑫
                choices.append(p['phrase']) # -----------------⑫
        # choicesリストが空であればNoneを返す
        if (len(choices) == 0): # -----------------------------⑭
            return None
        # choicesリストからランダムに応答フレーズを抽出して返す
        return random.choice(choices) # -----------------------⑮

    def suitable(self, need, mood): # -------------------------⑯
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


#### 以下、変数確認用のコード ####
if __name__ == "__main__":
    # 確認用コード：辞書オブジェクトの中身を出力
    d = Dictionary()
    # ランダム辞書
    print('Dictionary.random:', d.random)
    # パターン辞書
    for m in d.pattern:
        print('Dictionary.pattern.modify:', m.modify)
        print('Dictionary.pattern.pattern:', m.pattern) 
        print('Dictionary.pattern.phrases:', m.phrases)
    print(d.pattern)