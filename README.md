# Podcast-BE

To run podcast generation:
```
source setup_env.sh
python src/gen_podcast.py -o "Pretencious" -t "The Anthropic AI Hackathon" -d 2
```

To run high quality podcast generation:
```
python src/gen_podcast.py -o "Pretencious" -t "The Anthropic AI Hackathon" -d 2
```

To run server:

```
source setup_env.sh
python src/server.py
```

Run 
```
cp .env.example .env
```

And then edit the 
`.env` file to include the following keys:

```
OPENAI_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-west-2
ANTHROPIC_API_KEY=

```
