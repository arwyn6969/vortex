from src.core.user_profiling import ProfileMatrix, ProfileDimension
import numpy as np
from datetime import datetime, timedelta

def demonstrate_profiling():
    # Create profile matrix
    pm = ProfileMatrix()

    # Simulate user interactions over time
    user_id = 'demo_user'
    pm.create_profile(user_id)

    # Simulate correlated dimensions
    for i in range(30):
        # Empathy and social awareness are correlated
        base_value = np.sin(i / 5.0) * 0.3 + 0.5
        pm.update_profile(user_id, ProfileDimension.EMPATHY, base_value + np.random.normal(0, 0.1), 0.8)
        pm.update_profile(user_id, ProfileDimension.SOCIAL_AWARENESS, base_value + np.random.normal(0, 0.1), 0.8)
        
        # Creativity and emergent creativity are correlated differently
        creative_base = np.cos(i / 4.0) * 0.4 + 0.5
        pm.update_profile(user_id, ProfileDimension.CREATIVITY, creative_base + np.random.normal(0, 0.1), 0.7)
        pm.update_profile(user_id, ProfileDimension.EMERGENT_CREATIVITY, creative_base + np.random.normal(0, 0.1), 0.7)

    # Get adaptive dimension groups
    print('\nAdaptive Dimension Groups:')
    for i, group in enumerate(pm.dimension_clusters.get(user_id, [])):
        print(f'Group {i + 1}:', ', '.join(dim.value for dim in group))

    # Get predictions for empathy
    predictions = pm.predict_future_behavior(user_id, ProfileDimension.EMPATHY, horizon_days=3)
    print('\nPredictions for Empathy (next 3 days):')
    for i in range(min(5, len(predictions['dates']))):  # Show first 5 predictions
        print(f'Time: {predictions["dates"][i].strftime("%Y-%m-%d %H:%M")}')
        print(f'Predicted: {predictions["predictions"][i]:.3f}')
        print(f'Range: [{predictions["lower_bound"][i]:.3f}, {predictions["upper_bound"][i]:.3f}]')

    # Show current profile state
    profile = pm.get_profile(user_id)
    print('\nCurrent Profile State:')
    for dim in [ProfileDimension.EMPATHY, ProfileDimension.SOCIAL_AWARENESS, 
                ProfileDimension.CREATIVITY, ProfileDimension.EMERGENT_CREATIVITY]:
        print(f'{dim.value}: {profile.dimensions[dim]:.3f} (confidence: {profile.confidence_scores[dim]:.3f})')

if __name__ == '__main__':
    demonstrate_profiling() 