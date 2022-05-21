export type ObjectConstructor<T> = new () => T;

export class SingletonProvider<T> {
    private instance: T;
    private objectConstructor: ObjectConstructor<T>;

    constructor(con: ObjectConstructor<T>) {
        this.objectConstructor = con;
    }

    public getInstance(): T {
        if (this.instance == null) {
            this.instance = new this.objectConstructor();
        }

        return this.instance;
    }
}

export function createSingleton<T>(con: ObjectConstructor<T>): SingletonProvider<T> {
    return new SingletonProvider<T>(con);
}
