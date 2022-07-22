import * as React from "react";

export interface EllipsableContentProps {
    value: string;
    maxLength?: number;
}

export const EllipsableContent = ({value, maxLength = 20}: EllipsableContentProps) => {
    if (value.length <= maxLength) {
        return <>{value}</>;
    }
    return <>{value.substring(0, maxLength - 1) + '...'}</>;
}
