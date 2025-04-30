import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {

  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="FoodMVP - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>

    <Container>
      <h1 className={styles.title}>Доброго времени суток!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что из себя представляет данный проект?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Данный проект – по типу клона сайта food.ru, созданный лично мной с использованием возможностей Django.
            </p>
            <p className={styles.textItem}>
              Цель этого сайта — дать возможность пользователям создавать и хранить рецепты на онлайн-платформе. Кроме того, можно скачать список продуктов, необходимых для
              приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.
            </p>
            <p className={styles.textItem}>
              Чтобы использовать все возможности сайта — нужна регистрация. Проверка адреса электронной почты не осуществляется, вы можете ввести любой email.
            </p>
            <p className={styles.textItem}>
                Обновления в v2:
                <ol>
                    <li className={styles.textItem}>
                        Добавление возможности указания калорийности блюд.
                    </li>
                    <li className={styles.textItem}>
                        Добавление YouTube-видеоплеера, если пользователь захотел указать ссылку на туториал.
                    </li>
                    <li className={styles.textItem}>
                        Добавление возможности лайкать блюда и оставлять комментарии под рецептами и под самими комментариями.
                    </li>
                    <li className={styles.textItem}>
                        Добавление возможности лайкать комментарии других пользователей.
                    </li>
                    <li className={styles.textItem}>
                        Добавление более защищенной аутентификации с помощью JWT-токенов.
                    </li>
                    <li className={styles.textItem}>
                        Подключение Twilio для регистрации и аутентификации с помощью телефона.
                    </li>
                    <li className={styles.textItem}>
                        Подключение Celery, Redis для рассылки email.
                    </li>
                    <li className={styles.textItem}>
                        Добавление кеширования запросов на страницах.
                    </li>
                    <li className={styles.textItem}>
                        Добавление телеграм бота с уведомлениями об акциях. (Optional)
                    </li>
                    <li className={styles.textItem}>
                        Подключение Stripe, YouKassa и системы подписок для получения доступа к Premium рецептам или что-то типа того)))
                    </li>
                </ol>
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки на ресурсы
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Код проекта находится тут - <a href="https://github.com/forbxpg/foodgram" className={styles.textLink}>Github</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="https://t.me/forbxpg" className={styles.textLink}>Тимур</a>
            </p>
          </div>
        </aside>
      </div>

    </Container>
  </Main>
}

export default About

