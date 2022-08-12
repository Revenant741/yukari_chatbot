import re
import janome.tokenizer # janome.tokenizerをインポート

def analyze(text): # -----------------------------------------①
    """ 形態素解析を行う関数

    Parameters:
        text(str): 解析対象の文章。  
            
        Returns:
            strのlistを格納したlist:
                形態素と品詞のペアを格納した多重リスト。
  
    """    
    t = janome.tokenizer.Tokenizer() # Tokenizerオブジェクトを生成。
    tokens = t.tokenize(text)        # 形態素解析を実行。
    result = []                      # 解析結果の形態素と品詞を格納するリスト。
    
    # リストからTokenオブジェクトを1つずつ取り出す
    for token in tokens: # ----------------------------------②
        result.append(               # resultに追加する。
            [token.surface,          # 形態素を取得。
             token.part_of_speech])  # 品詞情報を取得。
    return(result)

def keyword_check(part): # ----------------------------------③
    """ 品詞が名詞であるか調べる関数

    Parameters:
        part(str): 形態素解析の品詞の部分。  
            
        Returns:
            名詞であれば結果を格納したMatcオブジェクト、そうでなければNone。
            
    """
    return re.match( # -------------------------------------④
        '名詞,(一般|固有名詞|サ変接続|形容動詞語幹)',
        part
        )
