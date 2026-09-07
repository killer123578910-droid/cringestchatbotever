#import llm;


#take top k similarity, form its content to a context text;

#create system prompt like:"Bạn là một trợ lý ảo am hiểu thông tin. 
    #Dựa vào các thông tin sau đây: {context_text}
    #Hãy trả lời câu hỏi của người dùng: {user_query}.
    #Nếu thông tin không có trong ngữ cảnh, hãy nói rằng bạn không biết, tuyệt đối không bịa đặt."
    #and create option for user to input (like 1 for custom prompt, 2 for short,straight queríes)

#put prompt for llm do generate answer. response answer.