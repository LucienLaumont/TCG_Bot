def compare_numeric_values(target_str, guessed_str):
    """Comparer les valeurs numériques des poids et tailles et retourner l'emoji approprié."""
    try:
        target_value = float(target_str.replace(",", ".").strip())
        guessed_value = float(guessed_str.replace(",", ".").strip())

        if guessed_value < target_value:
            return "⬆️"
        elif guessed_value > target_value:
            return "⬇️"
        else:
            return "🟩"
    except (ValueError, TypeError):
        # Si la conversion échoue, retourner un emoji de base pour signaler une erreur
        return "❓"