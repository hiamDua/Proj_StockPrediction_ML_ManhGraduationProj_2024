Giữa/Cuối tháng 11: 
```
Yêu cầu của đề tài là phân tích dự báo giá chứng khoán của các công ty trong 1 ngành (IT, Banking, Invester..), cho nên em phải liệt kê tất cả các công ty trong khối ngành công nghệ thông tin ở VN. Sau đó sẽ lựa chọn các công ty này để lấy dữ liệu. Không giới hạn ở 10 công ty, có thể nhiều hơn hoặc ít hơn.
Về phần dữ liệu mua bán bằng 0, điều đó thường gặp ở các mã chứng khoán. Chúng ta phải phân tích cho từng mã cụ thể, từng thời điểm cụ thể để sử dụng các kỹ thuật cho phù hợp. 
- Nếu trong thời kỳ covid, tần suất mua bán bằng 0 nhiều (chứng minh nhiều) ta tách thời kỳ covid ra và phân tích tác động của covid đến giá chứng khoán, hoặc phân tích khả năng phục hồi của công ty sau thời kỳ covid.
- Nếu xuất hiện lặp đi lặp lại (ví dụ chủ nhật không có giao dịch) thì bỏ qua, và chỉ tính các ngày trong tuần, ngày chủ nhật không đưa vào tính toán
- Nếu xuất hiện rải rác một số ngày nào đó, tùy vào từng mô hình ARIMA – yêu cầu dữ liệu chuỗi thời gian liên tục vì vậy cần phải nội suy hoặc điền giá trị bị thiếu, Prophet: có thể tự động điều chỉnh mô hình theo sự gián đoạn, với LSTM cần đảm bảo dữ liệu được chuẩn hóa
- Có thể tạo biến giả (Dummy Variables) cho ARIMA và LSTM, tạo biến giả cho những ngày không có số liệu, biểu diễn chúng dưới dạng biến số phụ trợ giúp mô hình hiểu rằng có một khoảng trông trong dữ liệu




Mua bán theo cặp: (pair trading), hai cổ phiếu thường có mối quan hệ tương quan chặt chẽ, tức là chúng thường di chuyển theo cùng một xu hướng (cùng tăng hoặc cùng giảm). Điều này có thể xảy ra do chúng hoạt động trong cùng một ngành, có mô hình kinh doanh tương tự, hoặc bị ảnh hưởng bởi những yếu tố chung trong thị trường. Ví dụ FPT Software và TMA Software có thể là một cặp có tương quan, vì cả hai đều là công ty công nghệ. bChênh lệch giá (Spread): Trong giao dịch theo cặp, điều quan trọng là quan sát sự chênh lệch giá giữa hai cổ phiếu. Thay vì tập trung hoàn toàn vào việc một cổ phiếu tăng và cổ phiếu kia giảm, trader sẽ chú ý đến sự bất thường trong chênh lệch giá giữa hai cổ phiếu. Khi khoảng cách này lớn hơn bình thường (vì một cổ phiếu tăng nhiều hơn hoặc giảm nhiều hơn so với cổ phiếu kia), trader sẽ kỳ vọng rằng thị trường sẽ điều chỉnh trở lại sự tương quan quen thuộc. Chiến lược Long/Short: Khi sự chênh lệch trở nên bất thường, trader sẽ thực hiện một chiến lược long/short. Cụ thể: Long (mua) cổ phiếu được cho là bị "định giá thấp" (trong ví dụ của bạn là TMA Software khi giá giảm). Short (bán khống) cổ phiếu được cho là bị "định giá cao" (trong ví dụ là FPT Software khi giá tăng). Khi sự chênh lệch trở lại mức bình thường, trader sẽ đóng vị thế của mình và thu lợi nhuận từ sự điều chỉnh đó. Quay lại trạng thái cân bằng (Mean Reversion): Giao dịch theo cặp dựa trên giả định rằng giá của hai cổ phiếu có xu hướng quay lại trạng thái cân bằng sau một thời gian biến động bất thường. Khi sự chênh lệch giá quá lớn, trader kỳ vọng sự phục hồi của mối tương quan và từ đó kiếm lời.
```

Cuối T11 - đầu T12
```
thầy kêu mình làm cái quan hệ mua bán theo cặp tốt rồi, 
bây giờ sẽ cần phải làm 

3. Report
1. phải dự đoán giá cổ phiếu của 10 cái chứng khoán đó bằng ít nhất 3 loại mô hình ( lstm model, arima, liner, Prophet) rồi dựa vào cái chỉ số  RMSE, MAE, MSE để kiếm tra cái mô hình tốt nhất cho 10 cái cổ phiếu đó.
Và cái 1 bảng so sánh kết quả giữa dự đoán với thực tế như thế này của mỗi data 

2. Ứng dụng mua bán theo cặp:
chọn ra 2 cặp tiêu biểu của 2  Trading Reversal và Pair Trading: 
vd : Pair Trading lấy FPT và CMG  
Kịch bản: 
+ giá tb cổ phiếu FPT: 89,112 đồng
+ giá tb cổ phiếu CMG 42,353 đồng ( trong code)
mua 1000 cp mỗi loại trong 100 ngày tiếp theo anh sẽ đưa ra quyết định mua hay bán, xong 100 ngày sẽ thống kê là lời bao nhiêu lỗ bao nhiêu rồi đưa ra kết luận
Trading Reversal  cũng sẽ như thế
```



SỬA REPORT: 

```
+ Sản phẩm web: 
	- Dự đoán giá chứng khoán của 10 loại  
	- 100 ngày mua bán chứng khoán theo cặp của 5 cặp chứng khoán của mình crawl về rồi đưa ra chiến lược cho người dùng ( kịch bản giống 2 cặp ví dụ 1000 cổ phiếu mỗi loại 100 ngày) 

+ Viết đồ án 
1. Lưu ý khi viết cuốn:
Phải theo chuẩn IEEE chú thích là kiểu [1] 
2. Lưu ý khi viết đồ án:

- Chương 1: Tổng quan về nghiên cứu
Viết theo chuẩn IEEE
Gộp trong nước và ngoài nước thành 1 đoạn văn ( phải ít nhất 20 bài trong và ngoài nước )

=======================


- Chương 2: Mô tả bài toán và khung nghiên cứu
2.1 mô tả bài toán gồm 3 ý
	+ Phân tích theo cặp
	+ Tìm mô hình dự báo tốt nhất cho từng loại chứng khoán
	+ Ứng dụng 2 ý trên để thực hiện thí nghiệm 100 ngày
2.2.1 Khung nghiên cứu
+ Vẽ lại khung nghiên cứu cho đẹp hơn
+ chỉ sử dụng những gì mình làm( không có Prophet thì không thêm vào, Evaluation metrics cũng thế)

- Chương 3:  Thu thập và tiền xử lý dữ liệu
+ thêm phân tích khám phá

- Chương 4: Mua bán theo cặp
+ Nhớ thêm ma trận trong code ra
+ Cải tiến phần phân tích và kết luận bên readme.md vẫn còn thiếu
- Chương 5: Lựa chọn mô hình dự báo tốt nhất cho 10 chứng khoán
+ Viết công thức của ARIMA, LSTM, Ridge Regression không nói lý thuyết suông
---------------------
	Bảng chi tiết đánh giá theo từng cổ phiếu đã được hoàn thiện ( làm rất tốt) Nhưng mà cần phải giải thích:
		Dựa vào cái gì cho đó là tốt nhất? (r^2 cao, %mape thấp là mô hình tốt đúng không ?) %MAPE thấp thì ảnh hưởng gì 
			R^2 là gì?, %MAPE là gì?
	Quan trọng là nổi bật thông số, vẫn phải có cột nhận xét
- Chương 6: Đánh giá kết quả và ứng dụng thực tế ( làm luôn web) 
+ Mô tả thí nghiệm 100 ngày (  Pair Trading Strategy và Reversal Trading Strategy ) 
	LƯU Ý: Phải kết hơp 2 bài toán là
		+ Phân tích theo cặp
		+ Tìm mô hình dự báo tốt nhất cho từng loại chứng khoán
	Để sử dụng cho thí nghiệm này
- Kết luận và kiến nghị
- Tài liệu tham khảo
```