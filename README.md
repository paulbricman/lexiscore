![](https://paulbricman.com/assets/img/lexiscore_cover.png)
# Lexiscore

As a first effort in tackling the theme of information overload in content consumption, I've been working on the lexiscore: a nutritional label for food for thought designed to help you narrow in on resources which personally bring you the most value.

[Read more...](https://paulbricman.com/thoughtware/lexiscore)

# Installation

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