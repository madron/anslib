docker build -t mtek/riemann roles/docker/mtek/riemann/files/docker/

docker run -it --rm --name riemann mtek/riemann