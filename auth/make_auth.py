import json

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": "SAPISIDHASH 1775241238_ceaab5d072c1db915c415210a44cb0a4a3d44f90_u SAPISID1PHASH 1775241238_ceaab5d072c1db915c415210a44cb0a4a3d44f90_u SAPISID3PHASH 1775241238_ceaab5d072c1db915c415210a44cb0a4a3d44f90_u",
    "content-type": "application/json",
    "cookie": "VISITOR_INFO1_LIVE=-hHKZhrBrcE; VISITOR_PRIVACY_METADATA=CgJMSxIEGgAgQQ%3D%3D; YSC=PwTVvkUPlzo; _gcl_au=1.1.1035841141.1775215267; PREF=tz=Asia.Colombo&f6=40000000&f7=100&f4=4000000&repeat=NONE&autoplay=true; __Secure-ROLLOUT_TOKEN=CIuflJrLxP6wVBCR66aCn7WRAxjl_c6Ak9KTAw%3D%3D; __Secure-1PSIDTS=sidts-CjUBWhotCQfmrBZsRfp8gpLsT5LHqaB4WoZbzFjyFywkMFTUX2A-QcDgRVy1kpz0EzVtPOwfABAA; __Secure-3PSIDTS=sidts-CjUBWhotCQfmrBZsRfp8gpLsT5LHqaB4WoZbzFjyFywkMFTUX2A-QcDgRVy1kpz0EzVtPOwfABAA; HSID=AC2s4F_pYo0HF_osi; SSID=A51QtxzCB83FxE0rU; APISID=N8h-GmtXiXi4T-y1/AiAA1O7jHuaiT_w0c; SAPISID=I1cMZpb72tztSyPn/ASuuenjn3KDCH3m99; __Secure-1PAPISID=I1cMZpb72tztSyPn/ASuuenjn3KDCH3m99; __Secure-3PAPISID=I1cMZpb72tztSyPn/ASuuenjn3KDCH3m99; LOGIN_INFO=AFmmF2swRQIgb0yOtgYd6LL-H31WWzDJcgy1RJeJBxJpCMDNL_Ka65MCIQC-9InVe2Xbzqef8cVNOSPQpEg3OmGd_ny3jtCM1GVpfw:QUQ3MjNmd2JRVE5xYWU2N25pNnZNQ3l0NWRjLTJ1Vk82YTV6ajhGMFdmWUpCbklkaE5HSWU3NVBidDhFOGZLc3dicnFJNUNEVVItVXNtNjFLWFZEUDkyUkVwMnBsalBlR1RHQjhBb1ZQajMwQ1BHSzhIZ0R4MGRGR3VsSmJ4RlEtdmR2VlQzQjI1aDNVNjlxS0NTOVFYOHczUEhOUDBMY0lB; SID=g.a0008giOHMowk115ZNa9nHnZbHiPU9CckdcfotgKIneSLt2cKT9cfDc_M0MN6SKCk-4KA_mPkAACgYKAV4SARUSFQHGX2MigUFXhDjxouiyWIXQV-s1hxoVAUF8yKqD27mGX9ci9srkRv8wITC60076; __Secure-1PSID=g.a0008giOHMowk115ZNa9nHnZbHiPU9CckdcfotgKIneSLt2cKT9cWN5QCcVFD4LyAOGmjkOacgACgYKARsSARUSFQHGX2MilM8LGg4nX_Pg8feEmyCPURoVAUF8yKoYgFAjBXnGT2v2kKydoBK20076; __Secure-3PSID=g.a0008giOHMowk115ZNa9nHnZbHiPU9CckdcfotgKIneSLt2cKT9cic5b3K6l5_LCE3vI4D1MsgACgYKAYMSARUSFQHGX2MivhM69AiCggbMLtQROPDaUxoVAUF8yKr269xeqPXAX5z2diVYyqNX0076; SIDCC=AKEyXzU4Kim7JUh_ZxoX45WgdtBHcVeL7BWiu0vd-UrVdFYg1BXhtusDL-gTWjdjDmy1SFMJOQ; __Secure-1PSIDCC=AKEyXzWhOTuWq23dmjlPLTW57culLdr1kiHJKB4jHZMQwN4RtXK9uXc_e0x5_PTgd9mPm7moWQ; __Secure-3PSIDCC=AKEyXzWw2vWtze4ox2EZkiB-gNdt-1WLqoaLTDw0BYwf34uswKuJNhRhoBMdESEIjUDjNw-15Q",
    "origin": "https://music.youtube.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "CgstaEhLWmhyQnJjRSjV-L_OBjIKCgJMSxIEGgAgQQ%3D%3D",
    "x-origin": "https://music.youtube.com"
}

with open("../browser.json", "w") as f:
    json.dump(headers, f, indent=2)

print("browser.json created!")