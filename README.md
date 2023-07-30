# Podcast-BE

To run podcast generation:
```
python src/generate/gen_podcast.py -d 5 -t "Social media and the brain" -o "Pretencious"
```

To run server:

```
source setup_env.sh
python src/server.py
```

Update 
`.env` file to include the following keys:

```
OPENAI_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-west-2
```
