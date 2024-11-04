<template>
  <header class="conteiner">
    <div class="logo">
      <a href="{% url 'main' %}"> AFK</a>
    </div>
    <div class="navbarBorder">
      <div class="navbar">
        <a href="{% url 'main' %}">Home</a>
        <a href="{% url 'events' %}">Events</a>
        <a href="#">Top</a>
        <a href="">Other</a>
      </div>
    </div>
    <div class="login">
      {% if user.is_authenticated %}
      {% if user.is_superuser %}
      <a href="{% url 'admin/users' %}"> Admin </a>
      {% endif %}
      <a href="{% url 'profile' user.id %}"> Profile </a>
      {% else %}
      <a href="{% url 'login' %}"> Sign in </a>
      {% endif %}
    </div>
  </header>
</template>

<script>
export default {
  name: 'MainPage',
}
</script>

<style></style>