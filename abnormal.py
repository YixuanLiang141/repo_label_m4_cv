import pandas as pd


def find_abnormal_subjects(
    input_path="input.csv",
    output_path="abnormal_subjects.csv"
):
    df = pd.read_csv(input_path)

    # 将 value 转换为数值，无法转换的设为 NaN
    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    # 去除 subject_id 或 value 缺失的行
    df = df.dropna(
        subset=["subject_id", "value"]
    ).copy()

    # 按 subject_id 计算最小值和最大值
    stats = (
        df.groupby("subject_id")["value"]
        .agg(["min", "max"])
        .reset_index()
    )

    # 判断：
    # 最小值 < 最大值的一半
    abnormal = stats[
        stats["min"] < stats["max"] / 2
    ].copy()

    # 只输出 subject_id
    result = abnormal[["subject_id"]].copy()

    # 保存
    result.to_csv(
        output_path,
        index=False
    )

    print(
        f"Found {len(result)} abnormal subjects."
    )

    return result

if __name__ == "__main__":
    find_abnormal_subjects('./weight.csv', './abnormal.csv')