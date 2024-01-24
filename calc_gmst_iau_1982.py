#! /usr/local/bin/python3.6
"""
グリニジ平均恒星時 GMST(= Greenwich Mean Sidereal Time)の計算
: IAU1982 版
  Date          Author          Version
  2016.06.15    mk-mode.com     1.00 新規作成
Copyright(C) 2018 mk-mode.com All Rights Reserved.
---
  引数 : 日時(UT1（世界時1）)
           書式：YYYYMMDD or YYYYMMDDHHMMSS
           無指定なら現在(システム日時)を UT1 とみなす。
"""
import math
from datetime import datetime


def gc2jd(ut1):
    year = ut1.year
    month = ut1.month
    day = ut1.day
    hour = ut1.hour
    minute = ut1.minute
    second = ut1.second
    # 1月,2月は前年の13月,14月とする
    if month < 3:
        year -= 1
        month += 12
    # 日付(整数)部分計算
    jd = int(365.25 * year) \
        + year // 400 \
        - year // 100 \
        + int(30.59 * (month - 2)) \
        + day \
        + 1721088.5
    # 時間(小数)部分計算
    t = (second / 3600 + minute / 60 + hour) / 24.0
    return jd + t


def calc_gmst(ut1):
    """ GMST（グリニッジ平均恒星時）計算
        : IAU1982理論(by David Vallado)によるもの
            GMST = 18h 41m 50.54841s
                 + 8640184.812866s T + 0.093104s T^2 - 0.0000062s T^3 
            (但し、 T = 2000年1月1日12時(UT1)からのユリウス世紀単位)
    :param  float  jd_ut1: UT1 に対するユリウス日
    :return datetime gmst: グリニッジ平均恒星時(単位:radian)
    """
    PI2 = math.pi * 2    # => 6.283185307179586
    D2R = math.pi / 180  # => 0.017453292519943295
    jd_ut1 = gc2jd(ut1)
    t_ut1 = (jd_ut1 - 2451545.0) / 36525
    gmst = 67310.54841 + (876600.0 * 3600.0 + 8640184.812866 + (0.093104 - 6.2e-6 * t_ut1) * t_ut1) * t_ut1
    gmst = (gmst * D2R / 240.0) % PI2
    if gmst < 0.0:
        gmst += PI2
    return gmst


def deg2hms(deg):
    """ 99.999° -> 99h99m99s 変換
    :param  float deg: degree
    :return string:    99 h 99 m 99.999 s
    """
    sign = ""
    h = int(deg / 15)
    _m = (deg - h * 15.0) * 4.0
    m = int(_m)
    s = (_m - m) * 60.0
    if s < 0:
        s *= -1
        sign = "-"
    return "{}{:2d} h {:02d} m {:06.3f} s".format(sign, h, m, s)


def _test():

    ut1 = datetime.utcnow()

    jd_ut1 = gc2jd(ut1)
    print("JD(UT1):", jd_ut1)
    gmst = calc_gmst(ut1)
    gmst_d = gmst * 180 / math.pi
    gmst_h = deg2hms(gmst_d)
    print((
    "GMST = {} rad.\n"
    "     = {} deg.\n"
    "     = {}"
    ).format(gmst, gmst_d, gmst_h))


if __name__ == "__main__":
    _test()