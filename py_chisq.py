import numpy as np
from scipy import stats
#from scipy import optimize
from scipy.optimize import newton
from scipy.special import chdtri

nc0 = 0.00001
w = None
N = 50
df = 1
sig_level = 0.05
power = 0.8

var_list = [w, N, df, sig_level, power]

def None_var_num_check(var_list = None):
    a = 0
    for i in var_list:
        if i is None:
            a += 1
    return a 

#print(None_var_num_check(var_list = var_list))
if(None_var_num_check(var_list = var_list) > 1):
    print('エラー：w, N, df, sig_level, power の中に'+
                  '数値の定まっていないものが２つ以上あります。' +
                  '１つに減らしてください')
    exit() # エラー発生による終了処理
elif(None_var_num_check(var_list = var_list) == 0):
    print('エラー：求めるべき変数がないため、プログラムを終了します。')
    exit() # エラー発生による終了処理

#py_pwr_chisq(w = NULL, N = 500, df = 2, sig_level = 0.05, power = 0.8)

# 辞書を使うかも考えたが、直感的に分かりやすい方にする。
# 戻り値のない関数で入力値を判定する。
def var_check(w = None, N = None, df = None, sig_level = None, power = None):
    if(w is not None and isinstance(w, float)):
        if(0 > w or w > 1):
            print('エラー：wは0～1の間の実数である必要があります。'+
                          'プログラムを終了します')
            exit() # エラー発生による終了処理
    elif(w is None):
        print('wは入力されていません。wを求めます')

    if(N is not None and N <= 0):
        print('エラー：Nは1以上の整数である必要があります。' +
                           'プログラムを修理します')
        exit() # エラー発生による終了処理
    elif(N is None):
        print('Nは入力されていません。Nを求めます')

    if(df is not None and df <= 0):
        print('dfには1以上の数字を入れて下さい')
    elif(df is None):
        print('エラー：dfは入力されていません。プログラムを終了します')
        exit() # エラー発生による終了処理

    if(sig_level is not None and isinstance(sig_level, float)):
        if(0 > sig_level or sig_level > 1):
            print('エラー：sig_levelは0～1の間のである必要があります'+
                       'プログラムを終了します。')
            exit() # エラー発生による終了処理
    elif(sig_level is None):
        print('エラー：sig_levelは入力されていません。プログラムを終了します')
        exit() # エラー発生による終了処理

    if(power is not None and isinstance(power, float)):
        if(0 > power or power > 1):
            print('エラー：powerは0～1の間の実数である必要があります' +
                       'プログラムを終了します。')
            exit() # エラー発生による終了処理
    else:
        print('powerは入力されていません。powerを求めます')

    
# 入力内容のチェック
var_check(w = w, N = N, df = df, sig_level = sig_level, power = power)

def py_pchisq(q = None, df = None, ncp = 0, lower_tail = True, log_p = False):
    if(ncp > 0):
        s = 1 - stats.ncx2.cdf(q, df, nc = ncp)
    else:
        s = 1 - stats.ncx2.cdf(q, df, nc = nc0)
    return s

#print(chdtri(1, 0.05)) # あってる
#print(1-stats.ncx2.cdf(chdtri(1, 0.05), 1, 20)) # あってる。Rのlower = Falseはpythonでは1-になる


#print(py_pchisq(q = 0.5, df = 2, ncp = 0.001, lower_tail = True, log_p = False))


def power_compute(w = None, N = None, df = None, sig_level = None, power = None):
    k = None
    # power を求める
    if(power is None):
        k = chdtri(df, sig_level) # パーセント点を求める
        k = py_pchisq(q = k, df = df, ncp = N*w**2) # パーセント点 k 以下の面積を求める
    return k

#print(power_compute(w = 0.2, N = 500, df = 1, sig_level = 0.05, power = None)) # あってる



k = chdtri(df, sig_level)
def obj_function(w = None, N = None, df = None, sig_level = None, power = None):
    return  py_pchisq(q = k, df = df, ncp = N*w**2) - power # パーセント点 k 以下の面積を求める


# w を計算する
if(w is None):

# obj_functionの挙動の確認
    for i in range(100000):
        #print('i = ', i)
        w0 = i/100000
#        print('w = ', w0)
        p = obj_function(w = w0, N = N, df = df, sig_level = sig_level, power = power)
#       print(p)
        if(abs(p) < 0.001):
            print('wの値は{0}です'.format(w0))
            exit() # 目的達成による終了処理

    if(p == False):
        for i in range(100000):
            #print('i = ', i)
            w0 = - i/100000
#           print('w = ', w0)
            p = obj_function(w = w0, N = N, df = df, sig_level = sig_level, power = power)
#           print(p)
            if(abs(p) < 0.001):
                print('wの値は{0}です'.format(w0))
                exit() # 目的達成による終了処理

    if(p is None):
        print('申し訳ありません、wの値は求められませんでした。')
        exit() # エラーによる終了処理



### 必要なNを求める
if(N is None):

    for i in range(100000):
        #print('i = ', i)
        N0 = i + 1
#        print('w = ', w0)
        p = obj_function(w = w, N = N0, df = df, sig_level = sig_level, power = power)
#       print(p)
        if(abs(p) < 0.001):
            print('Nの値は{0}です'.format(N0))
            exit() # 目的達成による終了処理

    if(p == False):
        for i in range(10000):
            #print('i = ', i)
            N0 = - i - 1
#           print('w = ', w0)
            p = obj_function(w = w, N = N0, df = df, sig_level = sig_level, power = power)
#           print(p)
            if(abs(p) < 0.001):
                print('Nの値は{0}です'.format(N0))
                exit() # 目的達成による終了処理

    if(p is None):
        print('申し訳ありません、Nの値は求められませんでした。')
        exit() # エラーによる終了処理


#def newton_method(ans_value = None, sleshhold_value = 0.0001, iter_times = 1000):
#    ans_value = 0.00001
#    for i in range(iter_times):
#        # 漸化式
#        b = ans_value - objective_function(q = k, df = df, N = N, w = ans_value, power = power)
#        b = ans_value - objective_function(q = k, df = df, N = N, w = 0.000001, power = power)
#        ans_value = b


#def w_compute(w = None, N = None, df = None, sig_level = None, power = None):
#    k = None
#    # w を求める
#    if(w is None):
#        k = stats.ncx2.ppf(sig_level, df, nc = nc0) # パーセント点を求める
#        k = py_pchisq(q = k, df = df, ncp = N*w**2) # パーセント点 k 以下の面積を求める
#    return k

#print(p_body(w = 0.2, N = 500, df = 2, sig_level = 0.05, power = None))

