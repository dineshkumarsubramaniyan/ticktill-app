# TickTill Android

This is a minimal Android WebView wrapper for the deployed TickTill app.

## URL to change

The app currently loads the deployed site from `BuildConfig.STREAMLIT_URL` in `app/build.gradle.kts`.

If your public app URL is different, update this line:

```kotlin
buildConfigField("String", "STREAMLIT_URL", "\"https://ticktill-app.streamlit.app/?visitor=kd\"")
```

## Build on GitHub

Push the repo, then open the `Build Android APK` workflow in GitHub Actions.
The generated debug APK will be available in the workflow artifacts.