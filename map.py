import pandas as pd

def filter_large_csv_by_stay_ids(input_file, output_file, key_col, chunksize=100_000):
    valid_ids = [220052]

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

def remove_columns_from_csv(data_file, output_file):

    df = pd.read_csv(data_file)

    df = df[["subject_id", "charttime", "value"]]

    df.to_csv(output_file, index=False)
    print(f"输出文件保存至：{output_file}")

def sort_csv_by_two_col(input_file, output_file, col1, col2):
    df = pd.read_csv(input_file)
    df.sort_values(by=[col1, col2], inplace=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":

    #filter_large_csv_by_stay_ids('../../icu/chartevents.csv', './map.csv', 'itemid')
    remove_columns_from_csv('./map.csv', './map.csv')
    sort_csv_by_two_col('./map.csv', './map.csv', 'subject_id', 'charttime')