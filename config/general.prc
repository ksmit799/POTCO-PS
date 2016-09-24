# Window options...
window-title Pirates Online Remake
icon-filename pirates.ico

model-path resources/
model-path resources/phase_2
model-path resources/phase_3
model-path resources/phase_4
model-path resources/phase_5

default-model-extension .bam

# Audio and Graphics
audio-library-name p3fmod_audio
preferences-filename config/preferences.json
want-improved-graphics 1
want-portal-cull 1
want-shaders 1
framebuffer-multisample 1
multisamples 2


texture-anisotropic-degree 16
smooth-lag 0.4

# DClass files...
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Server
game-server 127.0.0.1
server-port 7199
server-version piratesremake-1.0.0

#Resolution
win-size 800 600

# Disable cache
want-cache #f

# Disable tutorial
skip-tutorial 1

# Whitelist
want-whitelist #f

# Notify
default-directnotify-level info
