import pandas as pd

def filter_large_csv_by_stay_ids(input_file, output_file, key_col, chunksize=100_000):
    valid_ids = [221662, 221653, 221289, 221906]

    reader = pd.read_csv(input_file, chunksize=chunksize)
    first_chunk = True

    total_rows_kept = 0
    for i, chunk in enumerate(reader):
        filtered_chunk = chunk[chunk[key_col].isin(valid_ids)]
        total_rows_kept += len(filtered_chunk)

        if first_chunk:
            filtered_chunk.to_csv(output_file, index=False, mode='w')
            first_chunk = False
        else:
            filtered_chunk.to_csv(output_file, index=False, mode='a', header=False)

        print(f"✔ 已处理第 {i+1} 块，保留 {len(filtered_chunk)} 行")

    print(f"🎉 筛选完成，最终保留 {total_rows_kept} 行，保存至 {output_file}")

def rename(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    df = df[["subject_id", "starttime", "endtime", "itemid", "amount", "rate", "linkorderid", "patientweight"]]
    df.rename(columns={'itemid': 'item'}, inplace=True)
    df.rename(columns={'amount': 'doze'}, inplace=True)
    df.rename(columns={'linkorderid': 'infusionid'}, inplace=True)
    df.rename(columns={'patientweight': 'weight'}, inplace=True)

    mapping = {221662: 'dopamine', 221906: 'norepinephrine', 221289: 'epinephrine', 221653: 'dobutamine'}
    df["item"] = df["item"].map(mapping).fillna(df["item"])

    df.to_csv(output_csv, index=False)
    print(f"Done, result save to: {output_csv}")

def filter_infusion_duration(input_csv, output_csv):
    df = pd.read_csv(
        input_csv,
        parse_dates=['starttime', 'endtime']
    )

    grouped = df.groupby('infusionid')

    duration = (
        grouped['endtime'].transform('max')
        - grouped['starttime'].transform('min')
    )

    df = df[duration >= pd.Timedelta(hours=1)]

    df.to_csv(output_csv, index=False)

    return df

if __name__ == "__main__":

    filter_large_csv_by_stay_ids('../../icu/inputevents.csv', './adrenal.csv', 'itemid')
    rename('./adrenal.csv', './adrenal.csv')
    filter_infusion_duration('./adrenal.csv', './adrenal.csv')