const { spawn } = require("child_process");

// const python = spawn("python", [
//   "../scripts/set_llm.py",
//   "HUGGINGFACE",
//   "meta-llama/Meta-Llama-3-8B-Instruct",
//   "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",
// ]);

const text = `
Những cuốn tiểu thuyết của Ian Fleming
Khi còn đang phục vụ tại Phòng Tình báo Hải quân, Fleming đã lên kế hoạch trở thành một nhà văn, và từng nói với một người bạn, "Tôi sẽ viết truyện điệp viên kết thúc mọi câu chuyện gián điệp." Ngày 17 tháng 2 năm 1952, ông bắt tay viết cuốn tiểu thuyết James Bond đầu tiên của mình, Casino Royale, tại điền trang Goldeneya ở Jamaica, cũng là nơi Fleming viết tất cả các tác phẩm về Bond trong suốt tháng 1 và tháng 2 hàng năm. Ông khởi nguồn câu chuyện ngay trước đám cưới của mình với cô bạn gái đang mang thai Ann Chateris, để phân tâm bản thân khỏi lễ thành hôn sắp tới.
Sau khi hoàn thành bản thảo Casino Royale, Fleming đưa nó cho bạn mình (và sau này là biên tập viên) William Plomer đọc thử. Plomer rất thích bản thảo và gửi nó tới cho nhà xuất bản Jonathan Cape, nhưng không được họ đánh giá cao. Cape cuối cùng đã xuất bản cuốn sách vào năm 1953 theo lời giới thiệu của Peter, anh trai của Fleming, một cây bút chuyên viết về du lịch. Từ năm 1953 đến năm 1966, hai năm sau khi Fleming qua đời, mười hai tiểu thuyết và hai tuyển tập truyện ngắn đã được ra mắt. Trong đó, hai cuốn sách cuối cùng là The Man with the Golden Gun and Octopussy và The Living Daylights, được ấn bản sau khi di cảo. Jonathan Cape là đơn vị phát hành tất cả các tác phẩm tại Anh.`;

const python = spawn("python", ["../scripts/analyze_text.py", text]);
python.stdout.on("data", (data) => {
  console.log("out: ", data.toString());
});

python.stderr.on("data", (data) => {
  console.log("err: ", data.toString());
});
