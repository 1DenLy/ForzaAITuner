# 🏎️ ForzaAITuner

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=flat&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**ForzaAITuner** — это приложение для сбора, анализа и обработки телеметрии из игр серии Forza (в частности, Forza Horizon 4). Проект перехватывает UDP-пакеты, транслируемые игрой в реальном времени, анализирует поведение автомобиля (подвеска, скорость, ускорение) и помогает формировать оптимальные настройки тюнинга на основе собранных данных.

---

## ✨ Ключевые возможности

- 📡 **UDP Перехватчик**: Чтение и парсинг потока телеметрии из Forza Data Out.
- 💾 **Хранение данных**: Интеграция с PostgreSQL для сохранения гоночных сессий и конфигураций тюнинга.
- 📊 **Мониторинг гонки**: Отслеживание показателей автомобиля в реальном времени.
- 🖥️ **Графический интерфейс**: Удобный UI для управления сессиями и просмотра результатов (построен на архитектуре MVVM).
- 🐳 **Docker-контейнеризация**: Быстрое развертывание БД и окружения с помощью `docker-compose`.

---

## 🛠️ Стек технологий

- **Язык**: Python
- **Архитектура**: DDD (Domain-Driven Design), MVVM для UI
- **База данных**: PostgreSQL
- **Инфраструктура**: Docker
- **Интерфейс**: Собственный UI 

---
