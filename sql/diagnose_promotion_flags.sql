SELECT had_display, had_mailer, COUNT(*) AS rows
FROM dim_promotion
GROUP BY had_display, had_mailer;