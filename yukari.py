import random
import responder
import dictionary

class yukari(object):
    """ ピティナの本体クラス
    
    Attributes:
      name (str): Pitynaオブジェクトの名前を保持する。
      dictionary (obj:`Dictionary`): Dictionaryオブジェクトを保持する。
      emotion(obj:`Emotion`): Emotionオブジェクトを保持する。
      res_repeat (obj:`RepeatResponder`): RepeatResponderオブジェクトを保持する。      
      res_random (obj:`RandomResponder`): RandomResponderオブジェクトを保持する。      
      res_pattern (obj:`PatternResponder`): PatternResponderオブジェクトを保持する。      

    """
    def __init__(self, name):
        """ Pitynaオブジェクトの名前をnameに格納。
            Responderオブジェクトを生成してresponderに格納。
            
            Parameters:
                name(str): Pitynaオブジェクトの名前。
        """
        # Pitynaオブジェクトの名前をインスタンス変数に代入。
        self.name = name
        # Dictionaryを生成
        self.dictionary = dictionary.Dictionary()
        # Emotionを生成
        self.emotion = Emotion(self.dictionary.pattern) # ----------------①
        # RepeatResponderを生成
        self.res_repeat = responder.RepeatResponder('Repeat?')
        # RandomResponderを生成
        self.res_random = responder.RandomResponder(
                'Random', self.dictionary.random
                )
        # PatternResponderを生成
        self.res_pattern = responder.PatternResponder(
                'Pattern', self.dictionary
                )

    def dialogue(self, input):
        """ 応答オブジェクトのresponse()を呼び出して応答文字列を取得する。

            Parameters:
                input(str)  :ユーザーによって入力された文字列。  
            
            Returns:
                str: ピティナの応答フレーズ。
        """
        self.emotion.update(input) # ------------------------------------②
        # 1から100をランダムに生成
        x = random.randint(1, 100)
        # 60以下ならPatternResponderオブジェクトにする
        if x <= 90:
            self.responder = self.res_pattern
        # 61～90以下ならRandomResponderオブジェクトにする
        elif 90 <= x <= 95:
            self.responder = self.res_random
        # それ以外はRepeatResponderオブジェクトにする
        else:
            self.responder = self.res_repeat
        print(self.emotion.mood) ##### 機嫌値を確認したいときに使う #####
        return self.responder.response(input, self.emotion.mood) # -----②

    def get_responder_name(self):
        """ 応答に使用されたオブジェクト名を返す。
        
        Returns:
            str: 応答オブジェクトの名前。        
        """
        # responderに格納されているオブジェクト名を取得し戻り値にする。
        return self.responder.name

    def get_name(self):
        """ Pitynaオブジェクトの名前を返す。
               
        Returns:
            str: Pitynaクラスを示す文字列。        
        """
        # インスタンス変数nameの値を戻り値にする。 
        return self.name

class Emotion:
    """ ピティナの感情モデル
    
    Attributes:
      pattern (PatternItemのlist): [PatternItem1, PatternItem2, PatternItem3, ...]
      mood (int): ピティナの機嫌値を保持する。
      
    """
    # 機嫌値の上限／下限と回復値をクラス変数として定義
    MOOD_MIN = -15 # ---------------------------------------①
    MOOD_MAX = 15 # ----------------------------------------②
    MOOD_RECOVERY = 0.5 # ----------------------------------③

    def __init__(self, pattern): # -------------------------④
        """ 初期化メソッド
        
            ・Dictionaryオブジェクトのpatternをインスタンス変数dictionaryに格納。
            ・機嫌値moodを0で初期化する。

            Parameters:
                pattern(dec) :Dictionaryのpattern
                              (中身はPatternItemのリスト)
                
        """
        self.pattern = pattern
        self.mood = 0

    def update(self, input): # -----------------------------⑤
        """ 機嫌値を変動させるメソッド
            
            ・機嫌値をプラス/マイナス側にMOOD_RECOVERYのぶんだけ戻す。
            ・ユーザーからのメッセージをパターン辞書にマッチさせ、機嫌値を変動させる。

            Parameters:
              input(str) : ユーザーからのメッセージ
              
        """
        # 機嫌を徐々にもとに戻す処理。
        if self.mood < 0: # --------------------------------⑥
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0: # ------------------------------⑦
            self.mood -= Emotion.MOOD_RECOVERY
          
        # パターン辞書の各行の正規表現をユーザーのメッセージに繰り返しパターンマッチさせる。
        # マッチした場合はadjust_mood()で機嫌値を変動させる。
        for ptn_item in self.pattern: # --------------------⑧
            if ptn_item.match(input): # --------------------⑨
                self.adjust_mood(ptn_item.modify) # --------⑩
                break

    def adjust_mood(self, val): # --------------------------⑪
        """ 機嫌値を増減させるメソッド

            Parameters:
              val(int) : 機嫌変動値
              
        """
        # 機嫌値moodの値を機嫌変動値によって増減する
        self.mood += int(val)
        # MOOD_MAXとMOOD_MINと比較して、機嫌値が取り得る範囲に収める
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN
