import json
import random
import re

#     ("脅かす", "おびやかす"),
#     ("矛盾", "むじゅん"),
#     ("突如", "とつじょ"),
#     ("威力", "いりょく"),
#     ("奉仕", "ほうし"),
#     ("忠実", "ちゅうじつ"),
#     ("意欲", "いよく"),
#     ("車輪", "しゃりん"),
#     ("蒸気", "じょうき"),
#     ("限界", "げんかい"),
#     ("延長", "えんちょう"),
#     ("強いる", "しいる"),
#     ("記憶", "きおく"),
#     ("該当", "がいとう"),
#     ("印刷", "いんさつ"),
#     ("並行", "へいこう"),
#     ("組織", "そしき"),
#     ("交わす", "かわす"),
#     ("情報網", "じょうほうもう"),
#     ("誤り", "あやまり（ミス）"),
#     ("犯す", "罪をおかす"),
#     ("頭脳", "ずのう"),
#     ("端的", "たんてき"),
#     ("依存", "いぞん"),
#     ("著しい", "いちじるしい"),
#     ("甚だしい", "はなはだしい"),
#     ("無惨", "むざん"),
#     ("不慮", "ふりょ"),
#     ("疎外", "そがい"),
#     ("無視", "むし"),
#     ("粗暴", "そぼう"),
#     ("試行錯誤", "しこうさくご"),
#     ("阻止", "そし"),
#     ("馬力", "ばりき"),
#     ("勝る", "まさる"),
#     ("精巧", "せいこう"),
#     ("錯覚", "さっかく"),
#     ("陥る", "おちいる"),
#     ("魔法", "まほう"),
#     ("杖", "つえ"),
#     ("宝庫", "ほうこ"),
#     ("鈍い", "にぶい"),
#     ("創り出す", "（世界を）つくりだす"),
#     ("費やす", "ついやす"),
#     ("区別", "くべつ"),
#     ("貧困", "ひんこん"),
#     ("極めて", "きわめて"),
#     ("玩具", "がんぐ"),
#     ("涸渇", "こかつ"),
#     ("停滞", "ていたい"),
#     ("源泉", "（水の）げんせん"),
#     ("遂行", "すいこう　（やりとげる）"),
#     ("放棄", "ほうき"),
#     ("随分", "ずいぶん"),
#     ("探索", "（細かく）たんさく"),
#     ("萌芽", "ほうが"),
#     ("称する", "しょうする"),
#     ("知恵", "ちえ"),
#     ("焦る", "あせる"),
#     ("反省", "はんせい"),
#     ("価値", "かち"),
#     ("歩む", "あゆむ"),
#     ("継ぐ", "つぐ"),
#     ("馬鹿", "ばか"),
#     ("熱帯雨林", "ねったいうりん"),
#     ("絶滅", "ぜつめつ"),
#     ("落葉樹林", "らくようじゅりん"),
#     ("放牧", "ほうぼく"),
#     ("繁栄", "はんえい"),
#     ("循環", "じゅんかん"),
#     ("乾燥", "かんそう"),
#     ("耕作", "こうさく（農業）"),
#     ("過剰", "かじょう"),
#     ("破壊", "はかい"),
#     ("供給", "きょうきゅう"),
#     ("降雨", "こうう"),
#     ("数値", "すうち"),
#     ("燃料", "ねんりょう"),
#     ("脆弱", "ぜいじゃく"),
#     ("飢餓", "きが"),
#     ("沼", "ぬま"),
#     ("硫黄", "いおう"),
#     ("窒素", "ちっそ"),
#     ("硝酸", "しょうさん"),
#     ("沿岸", "えんがん"),
#     ("廃棄", "はいき"),
#     ("連鎖", "れんさ"),
#     ("濃縮", "のうしゅく"),
#     ("傷", "きず"),
#     ("規模", "きぼ"),
#     ("許容限度", "きょようげんど"),
#     ("浮遊", "ふゆう"),
#     ("人為的", "じんいてき"),
#     ("遺跡", "いせき"),
#     ("閉鎖", "へいさ"),
#     ("無秩序", "むちつじょ"),
#     ("巣", "（鳥の）す"),
#     ("敏感", "びんかん"),
#     ("省略", "しょうりゃく"),
#     ("仕掛け", "しかけ"),
#     ("電池", "でんち"),
#     ("放射", "ほうしゃ"),
#     ("構造", "こうぞう"),
#     ("混じる", "まじる　こんざつ"),
#     ("相互", "そうご"),
#     ("崩壊", "ほうかい"),
#     ("柔軟", "じゅうなん"),
#     ("排泄", "はいせつ"),
#     ("捉える", "とらえる　そくしん"),
#     ("烙印", "らくいん（をはる）"),
#     ("貼る", "はる"),


# ---------------- parsing helpers ----------------
def load_blocks() -> dict:
    with open("blocks.json", "r", encoding='utf-8') as f:
        return json.load(f)

def parse_range_string(s: str) -> list:
    """
    Accepts strings like:
      "15-17", "15,17,20-22", "30", "15-17 20"
    and returns a sorted list of unique integers.
    """
    s = s.strip()
    if not s:
        return []
    ns = set()
    for part in re.split(r'[,\s;]+', s):
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            ns.update(range(int(a), int(b) + 1))
        else:
            ns.add(int(part))
    return sorted(ns)

# ---------------- quiz runner ----------------
def run_quiz(blocks: dict):
    if not blocks:
        print("No blocks found. Make sure `raw_text` contains '# nNN' headers and entries.")
        return

    print("Available blocks:", blocks.keys())
    sel = input("Enter blocks or ranges (e.g. 15-17 or 15,17,20-22) -> ").strip()
    ns = parse_range_string(sel)
    if not ns:
        print("No blocks selected. Exiting.")
        return

    subset = []
    for n in ns:
        if n not in blocks:
            print(f"  Warning: block n{n} not found — skipping")
            continue
        subset.extend(blocks[n])

    if not subset:
        print("No vocabulary in selected blocks. Exiting.")
        return

    random.shuffle(subset)

    try:
        while True:
            wrong_answers = []  # store cards you got wrong

            for i, (kanji, reading) in enumerate(subset):
                pct = round(100 * (i + 1) / len(subset), 2)
                print(f"{pct}% — Reading: {reading}")
                cmd = input("Press Enter to reveal, or type 'q' to quit, 's' to skip -> ").strip().lower()
                if cmd == 'q':
                    print("Quitting.")
                    if wrong_answers:
                        print("\nYou got these wrong:")
                        for k, r in wrong_answers:
                            print(f"{k} ({r})")
                    return
                if cmd == 's':
                    print("-" * 30)
                    continue

                print(f"Kanji: {kanji}")
                got_it = input("Did you get it right? (Y/N) -> ").strip().upper()
                if got_it != 'Y':
                    wrong_answers.append((kanji, reading))
                print("-" * 30)

            if wrong_answers:
                print("\n❌ You got these wrong this round:")
                for k, r in wrong_answers:
                    print(f"{k} ({r})")
            else:
                print("\n✅ Perfect! You got everything right!")

            again = input("\nFinished. Start again with the SAME selection? (Y/N) -> ").strip().upper()
            if again != 'Y':
                break

    except KeyboardInterrupt:
        print("\nInterrupted. Bye.")

# ---------------- entry point ----------------
if __name__ == "__main__":
    # Option A (default): parse from the raw_text variable above
    blocks = load_blocks()
    run_quiz(blocks)

    