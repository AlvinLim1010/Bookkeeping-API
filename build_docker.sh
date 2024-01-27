echo "============Building image ================"
image_tag=${1:-latest}
image=backend:$image_tag
docker buildx build -t $image .

echo "============Building container ================"
docker compose up -d backend