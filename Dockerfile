FROM debian:12.2

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -q && \
    apt-get install -y -qq --no-install-recommends \
        biber \
        fonts-firacode \
        inkscape \
        make \
        perl \
        python3 \
        python3-json5 \
        python3-pip \
        python3-pygments \
        texlive-bibtex-extra \
        texlive-fonts-extra \
        texlive-lang-european \
        texlive-latex-base \
        texlive-latex-extra \
        texlive-pictures \
        texlive-science \
        wget
RUN pip3 install --break-system-packages makeish

RUN mkdir /workdir
RUN mkdir /workdir/doc
WORKDIR /workdir/doc

