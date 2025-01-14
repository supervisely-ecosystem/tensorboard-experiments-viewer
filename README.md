<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/12828725/228066998-7bd39e8a-562e-431e-a1b7-5940007f0ae7.jpg">

# View experiment metrics in Tensorboard

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> • 
  <a href="#Acknowledgment">Acknowledgment</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/tensorboard-logs-viewer)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/tensorboard-logs-viewer.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/tensorboard-logs-viewer.png)](https://supervisely.com)

</div>

## Overview

Run Tensorboard from the context menu of file (`*.tfevents.*`) or directory in Team Files.

# How To Use

1. Run app from the context menu of directory of file in **Team Files** -> `Run app` -> `Tensorboard`

2. Wait for the app to import your data (project will be created in the current workspace)

3. Stop app manually once you finish with it.

Here is an example how you could open a single `*.tfevents.*` file.

![Open a single file in Team files](https://user-images.githubusercontent.com/12828725/228075685-2946d65c-bba9-4a7e-90f7-66ee1cf5f77e.gif)

Here is an example how you could open a folder with multiple `*.tfevents.*` files.

![Open a directory with "*.tfevents.*" files in Team files](https://user-images.githubusercontent.com/78355358/236174364-af95b686-e355-4fd1-92c9-69331f72893d.gif)

# Acknowledgment

This app is based on the great repository [Tensorboard] (https://github.com/tensorflow/tensorboard) ![GitHub Org's stars](https://img.shields.io/github/stars/tensorflow/tensorboard?style=social) by tensorflow team .
