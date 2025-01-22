<div align="center" markdown>
<img src="https://github.com/user-attachments/assets/71d57891-8299-42ae-b007-3bd798624a52">

# View experiment metrics in Tensorboard

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> • 
  <a href="#Acknowledgment">Acknowledgment</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/tensorboard-experiments-viewer)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/tensorboard-experiments-viewer.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/tensorboard-experiments-viewer.png)](https://supervisely.com)

</div>

## Overview

Run Tensorboard from the context menu of file (`*.tfevents.*`) or directory in Team Files.

You can run this app only on files located in the `logs` directory with `*.tfevents.*` extension inside the artifacts directory of the training output or on the `logs` directory itself.

Example path to the `logs` directory: `/experiments/<project_id>_<project_name>/<task_id>_<framework>/logs/`

# How To Use

1. Run app from the context menu of directory or file in **Team Files** -> `Run app` -> `Tensorboard`

2. Wait for the tensorboard server to start. You will see a notification when the server is ready.

3. Stop app manually once you finish with it or it will be stopped automatically after 5 hours.

Here is an example how you could open a single `*.tfevents.*` file.

![Open a single file in Team files](https://user-images.githubusercontent.com/12828725/228075685-2946d65c-bba9-4a7e-90f7-66ee1cf5f77e.gif)

Here is an example how you could open a folder with multiple `*.tfevents.*` files.

![Open a directory with "*.tfevents.*" files in Team files](https://user-images.githubusercontent.com/78355358/236174364-af95b686-e355-4fd1-92c9-69331f72893d.gif)

# Acknowledgment

This app is based on the [Tensorboard](https://github.com/tensorflow/tensorboard) ![GitHub Org's stars](https://img.shields.io/github/stars/tensorflow/tensorboard?style=social) by tensorflow team .
