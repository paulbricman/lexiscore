![](https://paulbricman.com/assets/img/lexiscore_cover.png)
# Lexiscore

As a first effort in tackling the [theme of information overload](https://paulbricman.com/reflections/twenty-one) in content consumption, I've been working on the lexiscore: a nutritional label for food for thought designed to help you narrow in on resources which personally bring you the most value. The open source companion software can automatically label raw text originating from RSS feeds, bookmarked pages, PDFs, EPUBs, and more. In the scope of this project, I'm considering valuable resources to be those from which you learn a lot, those which are packed with ideas you find surprising.

[Read more...](https://paulbricman.com/thoughtware/lexiscore)

# Installation

**Note**: This tool requires a running instance of the [conceptarium](https://paulbricman.com/thoughtware/conceptarium) as a proxy for your knowledge.

The lexiscore labeler can either be deployed from source or using Docker.

### Docker

To deploy the lexiscore labeler using Docker, first make sure to have Docker installed, then simply run the following.

```
docker run -p 8501:8501 paulbricman/lexiscore 
```

The tool should be available at `localhost:8501`.

### From Source

To set up the lexiscore labeler, clone the repository and run the following:

```
python3 -m pip install -r requirements.txt
streamlit run main.py
```

The tool should be available at `localhost:8501`.

# Screenshots

![](https://paulbricman.com/assets/img/lexiscore_mockup.png)
![](https://paulbricman.com/assets/img/lexiscore_mealprep.png)
