Docker Desktop Windows

исправить путь
cd D:\Linux\microWakeWord-Trainer

исправить путь
docker run --rm -it --gpus all -p 8888:8888 -v D:\Linux\microWakeWord-Trainer:/data ghcr.io/tatertotterson/microwakeword:latest

docker run -d --name=rhvoice-rest -p 8080:8080 --restart unless-stopped ghcr.io/aculeasis/rhvoice-rest:latest

generate_samples.py
поправить TEXT OUTPUT_DIR


python generate_samples.py test

python generate_samples.py full

http://127.0.0.1:8888/lab

microWakeWord_training_notebook.ipynb
MAX_SAMPLES = 0 #Отключаем Piper