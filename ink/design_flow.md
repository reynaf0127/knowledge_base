## general setup
### 1. common.py: store general variables
### 2. find_list.py: grab staging db book list and topic lsit to summary and to answer


## branch workflow
### question topics
#### 3. question_answer.py: if it is a topic, LLM explain a question in details, no more than 1000 words, output is dataframe with topic and answer (n rows for each paragraph)

### book/paper
#### 4. word_count.py: 
#### 5. book_summary.py: if it is a book/paper, LLM summarize the content in details, no more than 1000 words, in n paragraph, output is datafram with book title, summary and quotes


## output generator
### 5. save_llmoutput.py: save csv file in local workspace as record to read and explore furthur topics to answer in deep level
### 6. nano_banana.py: use nano banana to generate pictures, n pictures per material
### 7. download_image.py: download pictures from url and save to vault
### 8. obsidian_notebook.py: create templated notebook per material and save to vault