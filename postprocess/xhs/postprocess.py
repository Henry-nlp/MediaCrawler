"""
从根目录运行程序。
"""

import os
import json
import asyncio
import datetime
from collections import Counter, OrderedDict
import csv

import sys
current_path = os.getcwd()
root_path = os.path.dirname(current_path)
sys.path.append(root_path)
sys.path.append(current_path)

import matplotlib.pyplot as plt



def plot_bar_chart(categories, values, save_words_prefix):
      # 绘制柱状图
      plt.bar(categories, values)

      # 添加标题和标签
      # plt.title('Bar Chart')
      plt.xlabel('Categories')
      plt.ylabel('Values')

      # 存储
      plt.savefig(f"./data/xhs/words/{save_words_prefix}_bar_chart.png", format='png', dpi=300)

      # 显示图形
      # plt.show()


def plot_line_chart(X, Y, save_words_prefix):
      # 绘制曲线图
      plt.plot(X, Y)

      # 添加标题和标签
      # plt.title('line Chart')
      plt.xlabel('X')
      plt.ylabel('Y')

      # 存储
      plt.savefig(f"./data/xhs/words/{save_words_prefix}_line_chart.png", format='png', dpi=300)

      # 显示图形
      # plt.show()


def json_to_csv(file_prefix, save_data):
      csv_path = os.path.join("./data/xhs/csv/", file_prefix + ".csv")

      with open(csv_path, mode='a+', encoding="utf-8-sig", newline="") as f:
            f.fileno()
            writer = csv.writer(f)
            writer.writerow(save_data[0].keys())
            for line_data in save_data:
                  writer.writerow(line_data.values())


def get_date(micro_timestamp):
      # 时间戳
      timestamp = micro_timestamp / 1000  # 将毫秒转换为秒
      # 转换为datetime对象
      dt_object = datetime.datetime.fromtimestamp(timestamp)
      print(dt_object)
      # 获取年月日
      date_Ymd = dt_object.strftime("%Y-%m-%d")
      date_Ym = dt_object.strftime("%Y-%m")
      date_Y = dt_object.strftime("%Y")

      # return date_Y, date_Ym, date_Ymd, dt_object
      return str(date_Y), str(date_Ym), str(date_Ymd), str(dt_object)


def save_dict_to_csv(file_prefix, data_dict):
      csv_path = os.path.join("./data/xhs/csv/", file_prefix + ".csv")

      with open(csv_path, mode='a+', encoding="utf-8-sig", newline="") as f:
            f.fileno()
            writer = csv.writer(f)
            writer.writerow(data_dict.keys())
            writer.writerow(data_dict.values())

      plot_bar_chart(data_dict.keys(), data_dict.values(), file_prefix)
      plot_line_chart(data_dict.keys(), data_dict.values(), file_prefix)


def save_date_results_to_csv(file_prefix, save_data_new):
      time_Y = [note["time_Y"] for note in save_data_new]
      counter = Counter(time_Y)
      time_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-time_Y", time_freq)
      
      time_Ym = [note["time_Ym"] for note in save_data_new]
      counter = Counter(time_Ym)
      time_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-time_Ym", time_freq)

      last_update_time_Y = [note["last_update_time_Y"] for note in save_data_new]
      counter = Counter(last_update_time_Y)
      time_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-last_update_time_Y", time_freq)

      last_update_time_Ym = [note["last_update_time_Ym"] for note in save_data_new]
      counter = Counter(last_update_time_Ym)
      time_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-last_update_time_Ym", time_freq)

      liked_count = [note["liked_count"] if "万" not in note["liked_count"] else note["liked_count"].replace("万", "")*10000 for note in save_data_new]
      counter = Counter(liked_count)
      count_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-liked_count", count_freq)

      collected_count = [note["collected_count"] if "万" not in note["collected_count"] else note["collected_count"].replace("万", "")*10000 for note in save_data_new]
      counter = Counter(collected_count)
      count_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-collected_count", count_freq)

      comment_count = [note["comment_count"] if "万" not in note["comment_count"] else note["comment_count"].replace("万", "")*10000 for note in save_data_new]
      counter = Counter(comment_count)
      count_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-comment_count", count_freq)

      share_count = [note["share_count"] if "万" not in note["share_count"] else note["share_count"].replace("万", "")*10000 for note in save_data_new]
      counter = Counter(share_count)
      count_freq = dict(sorted(counter.items(), key=lambda item: item[1]))
      save_dict_to_csv(file_prefix + "-share_count", count_freq)


async def plot_wordcloud(file_prefix, save_data):
      from store.xhs import xhs_store_impl

      words_path_prefix = os.path.join("./data/xhs/words/", file_prefix)

      # 针对note正文绘制词云图
      note_content = []
      for note in save_data:
            note["content"] = note.pop("desc")
            note_content.append(note)
      await xhs_store_impl.XhsJsonStoreImplement.WordCloud.generate_word_frequency_and_cloud(note_content, words_path_prefix + "-content")

      # # 针对note标题绘制词云图
      # note_title = []
      # for note in save_data:
      #       note["content"] = note.pop("title")
      #       note_title.append(note)
      # await xhs_store_impl.XhsJsonStoreImplement.WordCloud.generate_word_frequency_and_cloud(note_title, words_path_prefix + "-title")

      # # 针对tag、nickname绘制词云图
      # note_tag = []
      # note_nickname = []
      # for note in save_data:
      #       note_tag = note_tag + note["tag_list"].split(",")
      #       note_nickname.append(note["nickname"])
      # tag_freq = Counter(note_tag)
      # save_dict_to_csv(file_prefix + "-tag_freq", tag_freq)
      # nickname_freq = Counter(note_nickname)
      # save_dict_to_csv(file_prefix + "-nickname_freq", nickname_freq)      
      # await xhs_store_impl.XhsJsonStoreImplement.WordCloud.generate_word_cloud(tag_freq, words_path_prefix + "-tag")
      # await xhs_store_impl.XhsJsonStoreImplement.WordCloud.generate_word_cloud(nickname_freq, words_path_prefix + "-nickname")


def main(folder_path):
      json_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]

      save_data = []
      for path in json_files:
            if os.path.exists(path):
                  print("path exists")
                  with open(path, 'r', encoding='utf-8') as file:
                        save_data = save_data + json.loads(file.read())

      filename = os.path.split(json_files[0])[1]
      file_prefix = os.path.splitext(filename)[0] + "-combine"

      if os.path.exists(path):
            print("path exists")

            # 基于note id去重
            note_id_lst = []
            save_data_unique = []
            for item in save_data:
                  if item["note_id"] not in note_id_lst:
                        save_data_unique.append(item)
                        note_id_lst.append(item["note_id"])
        
            save_data_new = []

            for line_data in save_data_unique:
                  date_Y, date_Ym, date_Ymd, dt_object = get_date(line_data["time"])
                  line_data["time_Y"] = date_Y
                  line_data["time_Ym"] = date_Ym
                  line_data["time_Ymd"] = date_Ymd
                  line_data["time"] = dt_object
                  
                  date_Y, date_Ym, date_Ymd, dt_object = get_date(line_data["last_update_time"])
                  line_data["last_update_time_Y"] = date_Y
                  line_data["last_update_time_Ym"] = date_Ym
                  line_data["last_update_time_Ymd"] = date_Ymd
                  line_data["last_update_time"] = dt_object

                  save_data_new.append(line_data)

            # 将原始数据存储为csv文件
            # json_to_csv(file_prefix, save_data_new)

            # 将日期及对应帖子数存储为csv文件
            # save_date_results_to_csv(file_prefix, save_data_new)

            # 生成词云图
            asyncio.run(plot_wordcloud(file_prefix, save_data_new))


if __name__ == '__main__':
      # json_file_path = "./data/xhs/json/search_contents_2024-12-02（搜索关键词“中复村，长征”）.json"
      json_file_path = "./data/xhs/json/"
      main(json_file_path)