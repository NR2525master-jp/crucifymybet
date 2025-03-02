from supabase import create_client, Client
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
import numpy as np
from django.shortcuts import render

# 'home' ビューを定義
def home(request):
    return render(request, 'index.html')

# Supabase接続設定
def get_supabase_client():
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    return create_client(url, key)

# 学習データをSupabaseから取得
def fetch_training_data():
    supabase = get_supabase_client()
    response = supabase.table('training_data').select('*').execute()
    
    #print("Supabaseから取得したデータ:", response.data)  # 追加！    
    return response.data

# PyTorchモデルのクラス（変更なし）
class RankingModel(nn.Module):
    def __init__(self):
        super(RankingModel, self).__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

@csrf_exempt
def predict(request):
    if request.method == "POST":
        # フロントエンドからのデータ取得
        data = json.loads(request.body)
        oddsA, oddsB = data["oddsA"], data["oddsB"]

        # Supabaseから学習データを取得
        training_data = fetch_training_data()  # Supabaseからデータを取得
        df = pd.DataFrame(training_data)

        # デバッグ: カラム名を表示
        #print("カラム名:", df.columns)

        # デバッグ: 最初の数行を表示
        #print("データの最初の行:\n", df.head())

        # oddsA, oddsB だけを選択
        try:
            X = df[["oddsA", "oddsB"]]
            y = df["ranking"]
        except KeyError as e:
            return JsonResponse({'error': f"指定したカラムが見つかりません: {e}"}, status=500)

        # データのスケーリング
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # モデルの学習
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_scaled, y)

        xgb_model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, random_state=42)
        xgb_model.fit(X_scaled, y)

        # PyTorchモデル
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch_model = RankingModel().to(device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(torch_model.parameters(), lr=0.01)

        X_train_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(device)
        y_train_tensor = torch.tensor(y.values, dtype=torch.float32).view(-1, 1).to(device)

        for epoch in range(100):
            optimizer.zero_grad()
            outputs = torch_model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()

        # 入力データをスケーリング
        input_features = np.array([[oddsA, oddsB]])
        input_features_scaled = scaler.transform(input_features)

        # 予測処理
        rf_prediction = float(rf_model.predict(input_features_scaled)[0])
        xgb_prediction = float(xgb_model.predict(input_features_scaled)[0])

        torch_model.eval()
        input_tensor = torch.tensor(input_features_scaled, dtype=torch.float32).to(device)
        with torch.no_grad():
            torch_prediction = float(torch_model(input_tensor).item())

        # 個別の予測結果を返す
        return JsonResponse({
            "rf_prediction": rf_prediction,
            "xgb_prediction": xgb_prediction,
            "torch_prediction": torch_prediction
        })
