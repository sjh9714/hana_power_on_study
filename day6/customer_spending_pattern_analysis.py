from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


# =========================
# 한글 폰트 설정
# =========================
available_fonts = {font.name for font in font_manager.fontManager.ttflist}
for font_name in ["Malgun Gothic", "AppleGothic", "NanumGothic"]:
    if font_name in available_fonts:
        plt.rcParams["font.family"] = font_name
        break

plt.rcParams["axes.unicode_minus"] = False


def get_data_path():
    project_root = Path(__file__).resolve().parents[1]
    candidates = [
        project_root / "data" / "credit_card_transactions.csv",
        project_root / "step1" / "data" / "credit_card_transactions.csv",
    ]

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        "credit_card_transactions.csv 파일을 찾을 수 없습니다. "
        "data/ 또는 step1/data/ 폴더를 확인하세요."
    )


def show_plot():
    if plt.get_backend().lower() == "agg":
        plt.close()
    else:
        plt.show()


def load_transactions():
    data_path = get_data_path()
    print(f"[데이터 파일] {data_path}")

    df = pd.read_csv(data_path)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    required_columns = {"cc_num", "category", "amt"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"필수 컬럼이 없습니다: {sorted(missing_columns)}")

    return df


def analyze_customer_spending_patterns(df):
    # 고객별로 어떤 카테고리에 자주/많이 소비하는지 집계합니다.
    customer_category = (
        df.groupby(["cc_num", "category"])
        .agg(
            거래횟수=("amt", "count"),
            총소비금액=("amt", "sum"),
            평균소비금액=("amt", "mean"),
        )
        .reset_index()
    )

    top_category_by_count = (
        customer_category.sort_values(
            ["cc_num", "거래횟수", "총소비금액"],
            ascending=[True, False, False],
        )
        .drop_duplicates("cc_num")
        .set_index("cc_num")
    )

    top_category_by_amount = (
        customer_category.sort_values(
            ["cc_num", "총소비금액", "거래횟수"],
            ascending=[True, False, False],
        )
        .drop_duplicates("cc_num")
        .set_index("cc_num")
    )

    customer_summary = df.groupby("cc_num").agg(
        총소비금액=("amt", "sum"),
        평균소비금액=("amt", "mean"),
        거래횟수=("amt", "count"),
    )

    top_spenders = customer_summary.sort_values("총소비금액", ascending=False).head(10)
    top_spender_patterns = top_spenders.copy()
    top_spender_patterns["최다거래카테고리"] = top_category_by_count.loc[
        top_spender_patterns.index, "category"
    ]
    top_spender_patterns["최다거래카테고리횟수"] = top_category_by_count.loc[
        top_spender_patterns.index, "거래횟수"
    ]
    top_spender_patterns["최대소비카테고리"] = top_category_by_amount.loc[
        top_spender_patterns.index, "category"
    ]
    top_spender_patterns["최대소비카테고리금액"] = top_category_by_amount.loc[
        top_spender_patterns.index, "총소비금액"
    ]

    category_spend = df.groupby("category")["amt"].sum().sort_values(ascending=False)

    return customer_category, top_spender_patterns, category_spend


def print_analysis_result(customer_category, top_spender_patterns, category_spend):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 160)

    print("\n===== 고객 소비 패턴 분석 목적 =====")
    print("- 고객별로 어떤 카테고리에 자주 결제하는지 확인")
    print("- 고객별로 어떤 카테고리에 가장 많은 금액을 쓰는지 확인")
    print("- 식료품 중심, 여행/고액 결제 중심 같은 소비 성향 분류에 활용")

    print("\n===== 고객별/카테고리별 소비 패턴 TOP 20 (총소비금액 기준) =====")
    print(customer_category.sort_values("총소비금액", ascending=False).head(20))

    print("\n===== 상위 소비 고객 10명의 주요 소비 카테고리 =====")
    print(top_spender_patterns)

    print("\n===== 카테고리별 전체 소비 금액 =====")
    print(category_spend)

    print("\n===== 결과 읽는 방법 =====")
    print("- 거래횟수가 가장 많은 카테고리: 고객이 자주 이용하는 소비 영역")
    print("- 총소비금액이 가장 큰 카테고리: 고객이 가장 많은 돈을 쓰는 영역")
    print("- 평균소비금액이 큰 카테고리: 한 번 결제할 때 금액이 큰 소비 영역")


def draw_category_spend_chart(category_spend):
    plt.figure()
    category_spend.plot(kind="bar")
    plt.title("카테고리별 전체 소비 금액")
    plt.xlabel("카테고리")
    plt.ylabel("총 소비 금액")
    plt.xticks(rotation=45)
    plt.tight_layout()
    show_plot()


def main():
    df = load_transactions()
    customer_category, top_spender_patterns, category_spend = (
        analyze_customer_spending_patterns(df)
    )

    print_analysis_result(customer_category, top_spender_patterns, category_spend)
    draw_category_spend_chart(category_spend)


if __name__ == "__main__":
    main()
