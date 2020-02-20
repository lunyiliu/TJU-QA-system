#TJU-QA-system
This is a Q&A Machine aiming to recommend restaurants for clients with multi-round Q&A. It uses two LSTM models to extract the named entities in user input and employs a Ti-idf model to classify the sentences. First it throw out question,analyzing the answer, and throws next question until it gets enough information to judge the recommended dishes, prices, restaurant names and address. In this process user could play with it or ask related questions. It will answer specific question.  
##The files here contain:
***Gensim_菜单-Gensim_食品_地点_店家归类:** Tf-idf models used in the chatbot, trained respectively for classfying menus,sentences,locations,etc.  
***NER模型: **The LSTM model used in named entity recognition for question answering, trained with 7500 input sentences.
***处理用户提问: **Handle user question and answer based on collected restaurant data, after the input sentence is parsed by NER models and Gensims.  
*前端: a web demo of the chatbot  
*前期版本: An earlier version of it  
*识别正向、负向食物: The LSTM model used in recommending final results  
*数据爬取: The scrawler used to collect local restaurants data on Meituan  
*主要模块: The dialog tree and the main entry of the program
