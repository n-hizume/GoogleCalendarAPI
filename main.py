from src.calendar_manager import CalendarManager
from src.load import load_creds, load_idlist
from src.define_format import decord_date, decord_datetime
from src.event import DateEvent, DatetimeEvent
import os

# 標準出力にて選択肢を数字で与えて入力を受け取る関数
def input_idx(list):
  size = len(list)
  for i in range(size):
    print(f'{i}: {list[i]}')
  idx = int(input())
  if idx < 0 or size <= idx:
    raise IndexError
  return idx

# accountフォルダに入っているフォルダ名を全て取得し、その中から選択してもらう。
def set_account(account_folder):
  accounts = [f for f in os.listdir(account_folder) if os.path.isdir(os.path.join(account_folder, f))]
 
  if len(accounts) < 2:
    return accounts[0]
  else:
    print('アカウント名を選択してください')
    return accounts[input_idx(accounts)]

# 標準入力でidリストのどの予定を追加するか選択してもらう。
def set_keys(keys):
  if len(keys) < 2:
      return keys[0]
  else:
    print('登録する予定を選んでください。')
    return keys[input_idx(keys)]

# タイトルを変更するなら標準入力で受け取る。
def set_title(key):
  title = ''
  print('タイトルを変更しますか？')
  idx = input_idx(['する', 'しない'])
  if idx == 0:
    print('タイトルを入力してください。')
    title = input()
  else:
    title = key
  
  return title


# 月を入力してもらう。
# 月が今月より小さい数字なら、年を+1
def set_year_and_month(today):
  print('月を入力してください')
  month = int(input())
  if month < today.month:
    return (today.year + 1), month
  else:
     return today.year, month

def main():

  # accountフォルダに入っているフォルダ名を全て取得
  account = set_account(account_folder='account')

  # ハンドラを用意
  manager = CalendarManager(account)
  # idlist.json の全てのキーを取得
  keys = manager.get_key_list()

  # ユーザーに終了してもらうまで一生続ける。
  while True:
    # マイカレンダーのどの予定かを選択、タイトルを確定
    key = set_keys(keys)
    title = set_title(key)

    # Googleカレンダーの予定のIDをidlist.jsonから取得
    event_id = manager.get_id(key)

    # 終日予定か時間ありの予定かを標準入力で受け取る。
    print('日時の形式を入力してください。')
    idx = input_idx(['終日', '時間指定', '時間指定(タイトルに時間を含める)'])


    #選択した予定について、0が入力されるまで日時を聞き続ける。
    while True:
      year, month = set_year_and_month(manager.today)
      if idx == 0:
        print('日付を「,」区切りで入力してください。(終了の場合、0を入力)')
      else:
        print('日付・時間を「,」区切りで入力してください。(終了の場合、0を入力)')

      data = input().replace(' ', '')
      if data == '0':
        break

      data = data.split(',')

      if idx == 0:
        for my_date in data:
          st_date, fn_date = decord_date(year, month, my_date)
          event = DateEvent(st_date=st_date, fn_date=fn_date, title=title)

      else:
        for my_datetime in data:
          st_datetime, fn_datetime = decord_datetime(year, month, my_datetime)
          if idx == 3:
            title_time = '(' + st_datetime.strftime('%H:%M') + '-' + fn_datetime.strftime('%H:%M') + ')'
            title += title_time
          event = DatetimeEvent(st_dtime=st_datetime, fn_dtime=fn_datetime, title=title)
      
      manager.write(event_id, event)

      print(f'\n・Registration Success：{event.title}=========================')
      print(event.get_term())
      print()

      
      print(f'まだ {account} の編集を続けますか？')
      idx = input_idx(['違う月を入力', '違う予定を入力', '終了'])
      if idx == 0:
        continue
      if idx == 1:
        break
      else:
        return
        

if __name__ == '__main__':
  main()

