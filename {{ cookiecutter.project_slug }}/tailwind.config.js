const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    content: ["./{{ cookiecutter.project_slug }}/templates/*.html", "./{{ cookiecutter.project_slug }}/templates/**/*.html"],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter var', ...defaultTheme.fontFamily.sans],
            },
        },
    }, plugins: [
        require('@tailwindcss/forms'),
    ],
}
