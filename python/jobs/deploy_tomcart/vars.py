# Restart - рестарт
# Clean - чистка томката с рестартом
# Stop - стоп
# Start - старт
# Deploy_axis - деплой axis приложений Tomcat с рестартом
# Deploy_axis2 - деплой axis приложений как и Deploy_axis, но другая папка  "\\\\sbt-oat-005\\Share1\\Zaglushki\\Deploy\\sec_axis"
# GetLog - получение логов
# Deploy_war - деплой war
operation=['Deploy_war','Restart','Clean','Stop','Start','Deploy_axis','Deploy_axis2','GetLog']


# Ветка заглушек
service_branch='master'

# Название сервиса должно совпадать с названием проекта
# Проект сервиса должен быть настроен под maven
service=''

# НТ1-old:
# tv-eribn-8r2-58,tv-eribn-8r2-59,tv-eribn-8r2-60,tv-eribn-8r2-61,tv-eribn-8r2-62,tv-eribn-8r2-63,tv-eribn-8r2-64,tv-eribn-8r2-65,tv-eribn-8r2-66,tv-eribn-8r2-67,tv-eribn-8r2-68,tv-eribn-8r2-69
# НТ2-old:
# erlik28,erlik29,erlik30,erlik31,erlik32,erlik33,erlik34,erlik35
# НТ1:
# tvli-erib0704,tvli-erib0705,tvli-erib0706,tvli-erib0707,tvli-erib0708,tvli-erib0709,tvli-erib0710,tvli-erib0711,tvli-erib0712,tvli-erib0713,tvli-erib0714,tvli-erib0715,tvli-erib0716,tvli-erib0717,tvli-erib0718,tvli-erib0719
# НТ2:
# tvli-erib0720,tvli-erib0721,tvli-erib0722,tvli-erib0723,tvli-erib0724,tvli-erib0725,tvli-erib0726,tvli-erib0727,tvli-erib0728,tvli-erib0729,tvli-erib0730,tvli-erib0731
# НТ3:
# tkli-erib0152,tkli-erib0153,tkli-erib0154,tkli-erib0155,tkli-erib0156,tkli-erib0157,tkli-erib0158,tkli-erib0159,tkli-erib0160,tkli-erib0161
servers='tvli-erib0704,tvli-erib0705,tvli-erib0706,tvli-erib0707,tvli-erib0708,tvli-erib0709,tvli-erib0710,tvli-erib0711,tvli-erib0712,tvli-erib0713,tvli-erib0714,tvli-erib0715,tvli-erib0716,tvli-erib0717,tvli-erib0718,tvli-erib0719'